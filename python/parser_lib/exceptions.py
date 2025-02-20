class UnexpectedTokenException(Exception):
    message = 'unexpected token "{}", expected "{}".'
    def __init__(self, unexpected: str, expected: str):
        super().__init__(self.message.format(unexpected, expected))

class SyntaxErrorException(Exception):
    message = 'syntax error at position {}:{}.'
    def __init__(self, line: int, column: int):
        super().__init__(self.message.format(line, column))

class UnexpectedCloseTagException(Exception):
    message = 'unexpected close tag.'
    def __init__(self):
        super().__init__(self.message)
