from pathlib import Path
from .lexer import scan
from .io import read_html_file

def parse(html_filepath: Path):
    html_content = read_html_file(html_filepath)
    tokens = scan(html_content)
    print(tokens)

    pass