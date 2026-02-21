import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


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
        self.assertEqual(node.props_to_html(), ' class="text"')

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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_value_required(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leaf_to_html_with_prop_1(self):
        node = LeafNode("p", "Hello, world!", {"id": "12345"})
        self.assertEqual(node.to_html(), '<p id="12345">Hello, world!</p>')
    
    def test_leaf_to_html_with_props_2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        result = node.to_html()
        self.assertIn('<a href="https://www.google.com">', result)
        self.assertTrue(result.endswith("Click me!</a>"))

if __name__ == "__main__":
    unittest.main()