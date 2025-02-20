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

    def scan(self) -> list[Token]:
        while True:
            if self.cursor == len(self.chars) - 1:
                self.tokens.append(Token(type_=TokenType.EOF, value=''))
                break

            if self.current_char == '>':
                self.tokens.append(Token(type_=TokenType.GT, value='>'))
                self.next_char()
                continue

            if self.current_char == '<':
                self.tokens.append(Token(type_=TokenType.LT, value='<'))
                self.next_char()
                continue

            if self.current_char == '/':
                self.tokens.append(Token(type_=TokenType.BAR, value='/'))
                self.next_char()
                continue

            if self.current_char.isalpha() and self.chars[self.cursor - 1] == '<':
                token_value = self.walk_chars_stream()
                self.tokens.append(Token(type_=TokenType.TAG_ID, value=token_value))
                continue

            if self.current_char.isalpha():
                token_value = self.walk_chars_stream()
                self.tokens.append(Token(type_=TokenType.TEXT, value=token_value))
                continue

            raise SyntaxErrorException(line=self.line, column=self.column)

        return self.tokens
    
    def next_char(self):
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