from enum import Enum

class TokenType(Enum):
    GT = '>'
    LT = '<'
    BAR = '/'
    TAG_ID = 'TAG_ID'
    TEXT = 'TEXT'
    EOF = 'EOF'

class Token:
    def __init__(self, type_: TokenType, value: str):
        self.type = type_
        self.value = value