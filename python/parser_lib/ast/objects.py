from enum import Enum
class AST:
    pass

class TagAttributeNode(AST):
    def __init__(self, key: str, value: str = ''):
        self.key = key
        self.value = value

    def __dict__(self):
        return {
            'key': self.key,
            'value': self.value
        }
        
class TagNode(AST):
    def __init__(self, tag_name: str, attributes: list[TagAttributeNode] = [], children: list[AST] = []):
        self.tag_name = tag_name
        self.attributes = attributes
        self.children = children

    def __dict__(self):
        return {
            'object_type': 'TAG',
            'tag_name': self.tag_name,
            'attributes': [attr.__dict__() for attr in self.attributes],
            'children': [child.__dict__() for child in self.children]
        }

class TextNode(AST):
    def __init__(self, text: str):
        self.text = text

    def __dict__(self):
        return {
            'object_type': 'TEXT',
            'value': self.text
        }