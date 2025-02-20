class AST:
    pass

class TagNode(AST):
    def __init__(self, tag_name: str, attributes: list[dict] = [], children: list[AST] = []):
        self.tag_name = tag_name
        self.attributes = attributes
        self.children = children

class HTMLNode(TagNode):
    def __init__(self):
        pass

class TextNode(AST):
    def __init__(self, text: str):
        self.text = text