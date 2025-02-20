from .token import Token, TokenType
from .exceptions import UnexpectedTokenException

def scan(html_content: str) -> list[Token]:
    chars = list(html_content)
    tokens = list[Token]()

    cursor = 0
    line = 1
    column = 1
    while True:
        if cursor == len(chars) - 1:
            tokens.append(Token(type_=TokenType.EOF, value=''))
            break

        if chars[cursor] == '\n':
            line += 1
            column = 0
            cursor += 1
            continue

        if chars[cursor] == ' ': # skip whitespace
            cursor += 1
            continue

        if chars[cursor] == '>':
            tokens.append(Token(type_=TokenType.GT, value='>'))
            cursor += 1
            continue

        if chars[cursor] == '<':
            tokens.append(Token(type_=TokenType.LT, value='<'))
            cursor += 1
            continue

        if chars[cursor] == '/':
            tokens.append(Token(type_=TokenType.BAR, value='/'))
            cursor += 1
            continue

        if chars[cursor].isalpha() and chars[cursor - 1] == '<':
            token_value = walk_chars_stream(chars, cursor)
            cursor += len(token_value)
            tokens.append(Token(type_=TokenType.TAG_ID, value=token_value))
            continue

        if chars[cursor].isalpha():
            token_value = walk_chars_stream(chars, cursor)
            cursor += len(token_value)
            tokens.append(Token(type_=TokenType.TEXT, value=token_value))
            continue

        raise UnexpectedTokenException(line=line, column=column, char=chars[cursor])

    return tokens

def walk_chars_stream(chars: list[str], cursor: int) -> str:
    text = str()
    while True:
        text += chars[cursor]
        cursor += 1
        if not chars[cursor].isalpha():
            break
    return text