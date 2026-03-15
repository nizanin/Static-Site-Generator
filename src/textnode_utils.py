from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:

        # Only split TEXT nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        # If delimiter not present, keep node as-is
        if delimiter not in text:
            new_nodes.append(node)
            continue

        parts = text.split(delimiter)

        # If even number of delimiters → invalid markdown
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid Markdown: missing closing delimiter '{delimiter}'")

        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes



