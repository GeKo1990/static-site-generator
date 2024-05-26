import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_eq1(self):
        node = TextNode("This is a text node", "bold", "My Url")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("This is a text node", "cursive", "https://boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://boot.dev")
        self.assertNotEqual(node, node2)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_node(self):
        text_node = TextNode("Sample text", TextType.TEXT.value)
        expected_leaf_node = LeafNode(None, "Sample text")
        self.assertEqual(text_node_to_html_node(text_node), expected_leaf_node)
    
    def test_bold_node(self):
        text_node = TextNode("Bold text", TextType.BOLD.value)
        expected_leaf_node = LeafNode("b", "Bold text")
        self.assertEqual(text_node_to_html_node(text_node), expected_leaf_node)
    
    def test_italic_node(self):
        text_node = TextNode("Italic text", TextType.ITALIC.value)
        expected_leaf_node = LeafNode("i", "Italic text")
        self.assertEqual(text_node_to_html_node(text_node), expected_leaf_node)
    
    def test_code_node(self):
        text_node = TextNode("Code text", TextType.CODE.value)
        expected_leaf_node = LeafNode("code", "Code text")
        self.assertEqual(text_node_to_html_node(text_node), expected_leaf_node)
    
    def test_link_node(self):
        text_node = TextNode("Link text", TextType.LINK.value, "http://example.com")
        expected_leaf_node = LeafNode("a", "Link text", {"href": "http://example.com"})
        self.assertEqual(text_node_to_html_node(text_node), expected_leaf_node)
    
    def test_image_node(self):
        text_node = TextNode("Image alt text", TextType.IMAGE.value, "http://example.com/image.png")
        expected_leaf_node = LeafNode("img", "", {"src": "http://example.com/image.png", "alt": "Image alt text"})
        self.assertEqual(text_node_to_html_node(text_node), expected_leaf_node)
    
    def test_invalid_text_type(self):
        text_node = TextNode("Unsupported text", "unsupported")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertTrue("unsupported is not supported" in str(context.exception))
    
    def test_none_text_node(self):
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(None)
        self.assertTrue("No TextNode provided" in str(context.exception))

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        should_be = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, should_be)
    
    def test_bold_delimiter(self):
        node = TextNode("This is text with **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        should_be = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, should_be)

    def test_italic_delimiter(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        should_be = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, should_be)

    def test_no_delimiter(self):
        node = TextNode("This is a plain text with no delimiters.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        should_be = [
            TextNode("This is a plain text with no delimiters.", TextType.TEXT)
        ]

        self.assertEqual(new_nodes, should_be)

    def test_unmatched_delimiter(self):
        node = TextNode("This is a text with an unmatched *italic delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertTrue("Unmatched delimiter" in str(context.exception))

    def test_multiple_delimiters(self):
        node = TextNode("This is **bold** and *italic* text", TextType.TEXT)
        
        # First split by bold delimiter
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        # Then split by italic delimiter
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)

        should_be = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, should_be)



if __name__ == "__main__":
    unittest.main()
