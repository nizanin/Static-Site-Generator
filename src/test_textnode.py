import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode_utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
 


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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "First")
        child2 = LeafNode("p", "Second")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><p>First</p><p>Second</p></div>"
        )

    def test_to_html_with_props(self):
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child], props={"class": "container"})
        result = parent.to_html()
        self.assertIn('<div class="container">', result)
        self.assertTrue(result.endswith("<span>text</span></div>"))

    def test_to_html_with_no_tag(self):
        child = LeafNode("span", "child")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_empty_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_children_must_be_list(self):
        with self.assertRaises(ValueError):
            ParentNode("div", "not-a-list")

    def test_nested_parentnodes_multiple_levels(self):
        leaf1 = LeafNode("i", "leaf1")
        leaf2 = LeafNode("b", "leaf2")
        child1 = ParentNode("span", [leaf1, leaf2])
        child2 = LeafNode("p", "child2")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><span><i>leaf1</i><b>leaf2</b></span><p>child2</p></div>"
        )

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")

    def test_link(self):
        node = TextNode("Google", TextType.LINK, url="https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_link_missing_url_raises(self):
        node = TextNode("Broken link", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, url="image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.png", "alt": "Alt text"})

    def test_image_missing_url_raises(self):
        node = TextNode("Alt text", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_unknown_type_raises(self):
        class FakeType:
            pass
        node = TextNode("???", FakeType)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_split(self):
        node = TextNode("Hello `code` world", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        assert result == [
            TextNode("Hello ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" world", TextType.TEXT),
        ]


    def test_bold_split(self):
        node = TextNode("Hello **bold** world", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        assert result == [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" world", TextType.TEXT),
        ]


    def test_italic_split(self):
        node = TextNode("Hello _italic_ world", TextType.TEXT)

        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        assert result == [
            TextNode("Hello ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" world", TextType.TEXT),
        ]


    def test_no_delimiter(self):
        node = TextNode("Hello world", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        assert result == [node]


    def test_missing_closing_delimiter(self):
        node = TextNode("Hello `code world", TextType.TEXT)

        try:
            split_nodes_delimiter([node], "`", TextType.CODE)
            assert False
        except Exception:
            assert True


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "![rick](https://img.com/rick.png) and ![morty](https://img.com/morty.png)"
        )
        self.assertListEqual(
            [
                ("rick", "https://img.com/rick.png"),
                ("morty", "https://img.com/morty.png")
            ],
            matches
        )

    def test_extract_no_images(self):
        matches = extract_markdown_images(
            "This text has no images"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev")],
            matches
        )

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "Visit [google](https://google.com) and [youtube](https://youtube.com)"
        )
        self.assertListEqual(
            [
                ("google", "https://google.com"),
                ("youtube", "https://youtube.com")
            ],
            matches
        )

    def test_extract_no_links(self):
        matches = extract_markdown_links(
            "There are no links here"
        )
        self.assertListEqual([], matches)


class TestSplitNodes(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )

        result = split_nodes_image([node])
        print(result)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            result
        )

    def test_multiple_images(self):
        node = TextNode(
            "![one](url1) and ![two](url2)",
            TextType.TEXT
        )

        result = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "url2"),
            ],
            result
        )

    def test_split_links(self):
        node = TextNode(
            "go to [boot.dev](https://boot.dev)",
            TextType.TEXT
        )

        result = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("go to ", TextType.TEXT),
                TextNode("boot.dev", TextType.LINK, "https://boot.dev")
            ],
            result
        )

    def test_multiple_links(self):
        node = TextNode(
            "[one](url1) and [two](url2)",
            TextType.TEXT
        )

        result = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "url1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.LINK, "url2"),
            ],
            result
        )






if __name__ == "__main__":
    unittest.main()