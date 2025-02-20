import pathlib

def read_html_file(path: pathlib.Path) -> str:
    with open(path, 'r') as html:
        return html.read()