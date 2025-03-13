from enum import Enum
from htmlnode import LeafNode
class TextType(Enum):
    NORMAL = "NORMAL"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"

class TextNode:
    def __init__(self, content, text_type, url=None):
        if text_type not in TextType:
            raise ValueError(f"invalid text type")
        if text_type == TextType.LINK and url is None:
            raise Exception("missing url")
        self.content = content
        self.text_type = text_type
        self.url = url

    def __eq__(self, target):
        return (
            self.text_type == target.text_type
            and self.content == target.content
            and self.url == target.url
        )
    
    def __repr__(self):
        return f"TextNode({self.content}, {self.text_type}, {self.url})"
        

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("invalid text type")
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.content)
        case TextType.BOLD:
            return LeafNode("b", text_node.content)
        case TextType.ITALIC:
            return LeafNode("i", text_node.content)
        case TextType.CODE:
            return LeafNode("code", text_node.content)
        case TextType.LINK:
            return LeafNode("a", text_node.content, {'href':text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.content})
