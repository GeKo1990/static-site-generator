import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from main import text_node_to_html_node


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

if __name__ == "__main__":
    unittest.main()
