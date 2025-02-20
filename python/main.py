from parser_lib.parser import Parser

HTML_FILEPATH = '../html_files/001.html'

def main():
    ast = Parser(HTML_FILEPATH).parse()

if __name__ == '__main__':
    main()