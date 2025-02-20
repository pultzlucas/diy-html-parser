from pathlib import Path
from .lexer import Lexer
from .io import read_html_file

def parse(html_filepath: Path):
    html_content = read_html_file(html_filepath)
    tokens = Lexer(html_content).scan()
    print(tokens)

    pass