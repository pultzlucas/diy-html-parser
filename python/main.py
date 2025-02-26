from parser_lib.parser import Parser
import json

HTML_FILEPATH = '../html_files/005.html'

def main():
    ast = Parser(HTML_FILEPATH).parse()

    with open('ast.json', 'w') as f:
        json.dump(ast.__dict__(), f, indent=2)


if __name__ == '__main__':
    main()