import unittest

from textnode import TextNode, TextType


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
            

if __name__ == "__main__":
    unittest.main()