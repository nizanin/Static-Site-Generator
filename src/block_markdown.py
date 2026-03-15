from enum import Enum
from htmlnode import HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node
from textnode_utils import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"     # plain text
    HEADING = "heading"         # start with 1-6 # characters
    CODE = "code"               # must start with 3 backticks
    QUOTE = "quote"             # must start with a "greater-than" character: > 
    UNORDERED_LIST = "unordered_list"  # must start with a - character
    ORDERED_LIST = "ordered_list"      # must start with a number followed by a . character and a space


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            cleaned_blocks.append(stripped)
    return cleaned_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    # Heading
    if block.startswith(tuple(["#" * i + " " for i in range(1, 7)])):
        return BlockType.HEADING

    # Code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote block
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list
    expected = 1
    for line in lines:
        if not line.startswith(f"{expected}. "):
            break
        expected += 1
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []

    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes

def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        # HEADING
        if block_type == BlockType.HEADING:
            level = block.count("#", 0, block.find(" "))
            text = block[level + 1:]

            children_nodes = text_to_children(text)
            children.append(HTMLNode(f"h{level}", None, children_nodes))


        # PARAGRAPH
        elif block_type == BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            children_nodes = text_to_children(text)

            children.append(HTMLNode("p", None, children_nodes))


        # QUOTE
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned = []

            for line in lines:
                cleaned.append(line.lstrip("> ").strip())

            text = " ".join(cleaned)
            children_nodes = text_to_children(text)

            children.append(HTMLNode("blockquote", None, children_nodes))


        # UNORDERED LIST
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            list_items = []

            for line in lines:
                text = line[2:]
                list_items.append(
                    HTMLNode("li", None, text_to_children(text))
                )

            children.append(HTMLNode("ul", None, list_items))


        # ORDERED LIST
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            list_items = []

            for line in lines:
                text = line.split(". ", 1)[1]
                list_items.append(
                    HTMLNode("li", None, text_to_children(text))
                )

            children.append(HTMLNode("ol", None, list_items))

        # BLOCK TYPE CODE
        elif block_type == BlockType.CODE:
            # Usuń tylko potrójne backticki
            code = block[3:-3]

            # usuń leading \n jeśli istnieje
            if code.startswith("\n"):
                code = code[1:]

            text_node = TextNode(code, TextType.TEXT)
            code_child = text_node_to_html_node(text_node)
            code_node = HTMLNode("code", None, [code_child])
            children.append(HTMLNode("pre", None, [code_node]))

    return HTMLNode("div", None, children)