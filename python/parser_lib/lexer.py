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

        if self.current_char == '>':
            self.next_char()
            return Token(type_=TokenType.GT, value='>')

        if self.current_char == '<':
            self.next_char()
            return Token(type_=TokenType.LT, value='<')

        if self.current_char == '/':
            self.next_char()
            return Token(type_=TokenType.BAR, value='/')

        if self.current_char.isalpha() and (self.chars[self.cursor - 1] == '<' or self.chars[self.cursor - 1] == '/'):
            stream = self.walk_chars_stream()
            return Token(type_=TokenType.TAG_ID, value=stream)

        if self.current_char.isalpha():
            stream = self.walk_chars_stream()
            return Token(type_=TokenType.TEXT, value=stream)

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

        if self.current_char == ' ': # skip whitespace
            self.next_char()
            return
        
    def walk_chars_stream(self) -> str:
        text = str()
        while True:
            text += self.current_char
            self.next_char()
            if not self.current_char.isalpha():
                break
        return text