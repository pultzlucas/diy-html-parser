class UnexpectedTokenException(Exception):
    message = 'unexpected token "{}" in position {}:{}.'
    def __init__(self, line: int, column: int, char: str):
        super().__init__(self.message.format(char, line, column))
