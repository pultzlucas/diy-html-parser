from .token import Token, TokenType
from .exceptions import SyntaxErrorException

class Lexer:
    def __init__(self, html_content: str):
        self.chars = list(html_content)
        self.cursor = 0
        self.line = 1
        self.column = 1
        self.tokens = list[Token]()
        self.current_char = self.chars[self.cursor]

    def next_token(self) -> Token:
        if self.current_char is None:
            return Token(type_=TokenType.EOF, value='')

        if self.current_char.isspace():
            self.skip_whitespaces()

        # TERMS
        
        if self.current_char.isalpha() and (self.see_behind() == '<' or self.see_behind() == '/'):
            stream = self.walk_chars_stream()
            return Token(type_=TokenType.TAG_ID, value=stream)

        if self.current_char.isalpha():
            stream = self.walk_chars_stream()
            if self.current_char == '=':
                return Token(type_=TokenType.ATTRIBUTE_KEY, value=stream)
            if self.current_char == '"':
                return Token(type_=TokenType.ATTRIBUTE_VALUE, value=stream)
            return Token(type_=TokenType.TEXT, value=stream)
        
        # SYMBOLS

        if self.current_char == '>':
            self.next_char()
            return Token(type_=TokenType.GT, value='>')

        if self.current_char == '<':
            self.next_char()
            return Token(type_=TokenType.LT, value='<')

        if self.current_char == '/':
            self.next_char()
            return Token(type_=TokenType.BAR, value='/')
        
        if self.current_char == '=':
            self.next_char()
            return Token(type_=TokenType.EQUALS, value='=')
        
        if self.current_char == '"':
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
        
    def walk_chars_stream(self) -> str:
        text = str()
        while self.current_char is not None and self.current_char.isalnum():
            text += self.current_char
            self.next_char()
        return text
    
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