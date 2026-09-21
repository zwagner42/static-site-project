from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "plain text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMAGE = "IMAGE"

class TextNode:

    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented

        return not (self.text != other.text or self.text_type != other.text_type or self.url != other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: 'TextNode'):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            if text_node.url:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            else:
                return LeafNode("a", text_node.text, {"href": ""})
        case TextType.IMAGE:
            if text_node.url:
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            else:
                return LeafNode("img", "", {"src": "", "alt": text_node.text})
        case _:
            raise Exception("Unknown TextType passed into text_node_to_html_node")
