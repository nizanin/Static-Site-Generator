from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"        # plain text
    BOLD = "bold"        # **Bold text**
    ITALIC = "italic"    # _Italic text_
    CODE = "code"        # `Code text`
    LINK = "link"        # [anchor text](url)
    IMAGE = "image"      # ![alt text](url)

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text              # content
        self.text_type = text_type    # member of TextType
        self.url = url                # default None

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    




def text_node_to_html_node(text_node):
    ttype = text_node.text_type
    text = text_node.text
    url = text_node.url

    if ttype == TextType.TEXT:
        return LeafNode(tag=None, value=text)

    elif ttype == TextType.BOLD:
        return LeafNode(tag="b", value=text)

    elif ttype == TextType.ITALIC:
        return LeafNode(tag="i", value=text)

    elif ttype == TextType.CODE:
        return LeafNode(tag="code", value=text)

    elif ttype == TextType.LINK:
        href = getattr(text_node, "url", None)
        if href is None:
            raise ValueError("LINK TextNode must have 'url'")
        return LeafNode(tag="a", value=text, props={"href": href})

    elif ttype == TextType.IMAGE:
        if url is None:
            raise ValueError("IMAGE TextNode must have 'url'")
        return LeafNode(tag="img", value="", props={"src": url, "alt": text})

    else:
        raise ValueError(f"Unknown TextType: {ttype}")