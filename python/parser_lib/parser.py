from pathlib import Path
from .lexer import Lexer
from .io import read_html_file
from .ast.objects import TagNode, TextNode, AST, TagAttributeNode
from .token import TokenType
from .exceptions import UnexpectedTokenException
class Parser:
    def __init__(self, html_filepath: Path):
        html_content = read_html_file(html_filepath)
        self.lexer = Lexer(html_content)
        self.current_token = self.lexer.next_token()

    def parse(self):
        node = self.html()
        if self.current_token.type != TokenType.EOF:
            raise UnexpectedTokenException(unexpected=self.current_token.type.value, expected=TokenType.EOF)
        return node

    def html(self) -> TagNode:
        node = self.tag()
        return node

    def tag(self) -> TagNode:
        self.__advance_token(TokenType.LT)
        tag_name = self.current_token.value
        self.__advance_token(TokenType.TAG_ID)

        tag_attributes = list[TagAttributeNode]()
        while True:
            if self.current_token.type == TokenType.ATTRIBUTE_KEY:
                attr = self.attribute()
                tag_attributes.append(attr)
                continue
            break

        if self.current_token.type == TokenType.BAR:
            self.__advance_token(TokenType.BAR)
            self.__advance_token(TokenType.GT)
            return TagNode(tag_name=tag_name, children=list(), attributes=tag_attributes)

        self.__advance_token(TokenType.GT)

        tag_children = list[AST]()
        while True:
            if self.current_token.type == TokenType.TEXT:
                tag_children.append(TextNode(text=self.current_token.value))
                self.__advance_token(TokenType.TEXT)
                continue
            if self.current_token.type == TokenType.LT:
                if self.lexer.chars[self.lexer.cursor] == TokenType.BAR.value: # is close tag
                    break
                node = self.tag()
                tag_children.append(node)
                continue
            break


        self.__advance_token(TokenType.LT)
        self.__advance_token(TokenType.BAR)
        self.__advance_token(TokenType.TAG_ID)
        self.__advance_token(TokenType.GT)

        return TagNode(tag_name=tag_name, children=tag_children, attributes=tag_attributes)
    
    def attribute(self) -> TagAttributeNode:
        attr = TagAttributeNode(key=self.current_token.value)
        self.__advance_token(TokenType.ATTRIBUTE_KEY)
        if self.current_token.type == TokenType.EQUALS:
            self.__advance_token(TokenType.EQUALS)
            self.__advance_token(TokenType.DOUBLE_QUOTE)
            attr.value = self.current_token.value
            self.__advance_token(TokenType.ATTRIBUTE_VALUE)
            self.__advance_token(TokenType.DOUBLE_QUOTE)
        return attr

    def __advance_token(self, expected_token_type: TokenType):
        if self.current_token.type != expected_token_type:
            raise UnexpectedTokenException(unexpected=self.current_token.type.value, expected=expected_token_type.value)
        self.current_token = self.lexer.next_token()