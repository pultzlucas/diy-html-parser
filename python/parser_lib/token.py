from enum import Enum

class TokenType(Enum):
    GT = '>'
    LT = '<'
    BAR = '/'
    DOUBLE_QUOTE = '"'
    EQUALS = '='

    EOF = 'EOF'
    TAG_ID = 'TAG_ID'
    TEXT = 'TEXT'
    ATTRIBUTE_KEY = 'ATTRIBUTE_KEY'
    ATTRIBUTE_VALUE = 'ATTRIBUTE_VALUE'

class Token:
    def __init__(self, type_: TokenType, value: str):
        self.type = type_
        self.value = value

    def __str__(self):
        return f'Token( type: {self.type}, value: {self.value} )'