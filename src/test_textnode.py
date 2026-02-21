import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none_vs_value(self):
        # url None vs ustawiony → nie są równe
        node1 = TextNode("Link", TextType.LINK)
        node2 = TextNode("Link", TextType.LINK, "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_different_text_type_1(self):
        # różny typ → nie są równe
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_different_text_type_2(self):
        # różny typ → nie są równe
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode(
            tag="p",
            value="Hello",
            props={"class": "text"}
        )
        self.assertEqual(node.props_to_html(), 'class="text"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            tag="a",
            value="Click",
            props={
                "href": "https://example.com",
                "target": "_blank"
            }
        )
        result = node.props_to_html()

        self.assertIn('href="https://example.com"', result)
        self.assertIn('target="_blank"', result)

    def test_props_to_html_no_props(self):
        node = HTMLNode(
            tag="div",
            value="Content",
            props=None
        )
        self.assertEqual(node.props_to_html(), '')

if __name__ == "__main__":
    unittest.main()