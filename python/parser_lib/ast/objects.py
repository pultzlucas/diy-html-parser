class AST:
    pass

class TagAttributesNode(AST):
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
        
class TagNode(AST):
    def __init__(self, tag_name: str, attributes: list[TagAttributesNode] = [], children: list[AST] = []):
        self.tag_name = tag_name
        self.attributes = attributes
        self.children = children


class HTMLNode(TagNode):
    def __init__(self):
        pass

class TextNode(AST):
    def __init__(self, text: str):
        self.text = text