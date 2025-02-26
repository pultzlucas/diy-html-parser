from .token import Token, TokenType
from .exceptions import SyntaxErrorException
import re
class Lexer:
    def __init__(self, html_content: str):
        self.chars = list(html_content)
        self.cursor = 0
        self.line = 1
        self.column = 1
        self.tokens = list[Token]()
        self.current_char = self.chars[self.cursor]
        self.is_inside_tag_config = False

    def next_token(self) -> Token:
        if self.current_char is None:
            return Token(type_=TokenType.EOF, value='')

        if self.current_char.isspace():
            self.skip_whitespaces()

        if self.match_ahead('<!--'):
            self.skip_comments()

        # TERMS
        
        if self.current_char.isalnum() and (self.see_behind() == '<' or self.see_behind() == '/'):
            return Token(type_=TokenType.TAG_ID, value=self.get_id())

        if self.current_char.isalnum() and self.see_behind() == '"' and self.is_inside_tag_config:
            return Token(type_=TokenType.ATTRIBUTE_VALUE, value=self.get_attribute_value())

        if self.current_char.isalnum() and self.is_inside_tag_config:
            return Token(type_=TokenType.ATTRIBUTE_KEY, value=self.get_attribute_key())

        if self.current_char.isalnum() and not self.is_inside_tag_config:
            return Token(type_=TokenType.TEXT, value=self.get_text_value())
        
        # SYMBOLS

        if self.current_char == '>':
            self.next_char()
            self.is_inside_tag_config = False
            return Token(type_=TokenType.GT, value='>')

        if self.current_char == '<':
            self.next_char()
            if self.current_char != '/':
                self.is_inside_tag_config = True
            return Token(type_=TokenType.LT, value='<')

        if self.current_char == '/':
            self.next_char()
            return Token(type_=TokenType.BAR, value='/')
        
        if self.current_char == '=':
            self.next_char()
            return Token(type_=TokenType.EQUALS, value='=')
        
        if self.current_char == '"':
            self.is_attribute_value = False
            self.next_char()
            return Token(type_=TokenType.DOUBLE_QUOTE, value='"')

        raise SyntaxErrorException(line=self.line, column=self.column)
    
    def next_char(self):
        if self.cursor == len(self.chars) - 1: # EOF
            self.current_char = None
            return

        self.cursor += 1
        self.column += 1
        self.current_char = self.chars[self.cursor]

        if self.current_char == '\n': # skip break line
            self.line += 1
            self.column = 1
            self.next_char()
            return

    def skip_whitespaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.next_char()

    def skip_comments(self):
        close_comment_pattern = '-->'
        while self.current_char is not None and not self.match_ahead(close_comment_pattern):
            self.next_char()

        for i in close_comment_pattern:
            self.next_char()
        
    def get_text_value(self) -> str:
        value = str()
        while self.current_char is not None and self.is_text_stream():
            value += self.current_char
            self.next_char()
        return value
    
    def get_attribute_key(self) -> str:
        key = str()
        while self.current_char is not None and self.is_id_stream():
            key += self.current_char
            self.next_char()
        return key
    
    def get_id(self) -> str:
        id = str()
        while self.current_char is not None and self.is_id_stream():
            id += self.current_char
            self.next_char()
        return id
    
    def get_attribute_value(self) -> str:
        value = str()
        while self.current_char is not None and self.is_attribute_value_stream():
            value += self.current_char
            self.next_char()
        return value
    
    def see_ahead(self):
        ahead_pos = self.cursor + 1
        if ahead_pos > len(self.chars) - 1:
            return None
        else:
            return self.chars[ahead_pos]
        
    def see_behind(self):
        behind_pos = self.cursor - 1
        if behind_pos > len(self.chars) - 1:
            return None
        else:
            return self.chars[behind_pos]
        
    def match_ahead(self, pattern: str):
        for i, char in enumerate(pattern):
            if self.chars[self.cursor + i] != char:
                return False
        return True
    
    def is_text_stream(self):
        return not not re.search(r"[^<>]", self.current_char)
    
    def is_id_stream(self):
        return not not re.search(r"\w+|-", self.current_char)
    
    def is_attribute_value_stream(self):
        return not not re.search(r'[^\"]', self.current_char)