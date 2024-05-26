import unittest

from htmlnode import LeafNode
from textnode import (
    TextNode, 
    TextType, 
    text_node_to_html_node,
    text_to_textnodes,
    split_nodes_delimiter, 
    extract_markdown_links, 
    extract_markdown_images, 
    split_nodes_link, 
    split_nodes_image
)

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

class TestSplitNodesFunctions(unittest.TestCase):
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

    def test_split_nodes_image(self):
        text_type_text = TextType.TEXT.value
        text_type_image = TextType.IMAGE.value
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        should_be = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode("second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ]

        self.assertEqual(new_nodes, should_be)

    def test_split_nodes_link(self):
        text_type_text = TextType.TEXT.value
        text_type_link = TextType.LINK.value
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        should_be = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
            TextNode(" and another ", text_type_text),
            TextNode("second link", text_type_link, "https://example.org"),
        ]

        self.assertEqual(new_nodes, should_be)

    def test_split_nodes_image_no_images(self):
        text_type_text = TextType.TEXT.value
        node = TextNode(
            "This is text without any images.",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        should_be = [node]

        self.assertEqual(new_nodes, should_be)

    def test_split_nodes_link_no_links(self):
        text_type_text = TextType.TEXT.value
        node = TextNode(
            "This is text without any links.",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        should_be = [node]

        self.assertEqual(new_nodes, should_be)
    
class TestExtractMarkdownImages(unittest.TestCase):
    def test_2_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        result = extract_markdown_images(text)
        should_be = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]

        self.assertEqual(result, should_be)

    def test_single_image(self):
        text = "Here is a single ![example](https://example.com/image.png) in the text."
        result = extract_markdown_images(text)
        should_be = [("example", "https://example.com/image.png")]

        self.assertEqual(result, should_be)

    def test_no_images(self):
        text = "This text contains no images."
        result = extract_markdown_images(text)
        should_be = []

        self.assertEqual(result, should_be)

    def test_images_with_special_characters(self):
        text = "An image with special characters ![special@image](https://example.com/image@name.png) and another ![image&with*chars](https://example.com/image&name*.png)."
        result = extract_markdown_images(text)
        should_be = [
            ("special@image", "https://example.com/image@name.png"),
            ("image&with*chars", "https://example.com/image&name*.png")
        ]

        self.assertEqual(result, should_be)

    def test_image_with_spaces(self):
        text = "An image with spaces in the alt text ![image with spaces](https://example.com/image.png)."
        result = extract_markdown_images(text)
        should_be = [("image with spaces", "https://example.com/image.png")]

        self.assertEqual(result, should_be)

    def test_multiple_lines(self):
        text = """
        This is text with multiple images:
        ![first image](https://example.com/first.png)
        Some text in between.
        ![second image](https://example.com/second.png)
        """
        result = extract_markdown_images(text)
        should_be = [
            ("first image", "https://example.com/first.png"),
            ("second image", "https://example.com/second.png")
        ]

        self.assertEqual(result, should_be)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "Here is a single [example](https://example.com) in the text."
        result = extract_markdown_links(text)
        should_be = [("example", "https://example.com")]

        self.assertEqual(result, should_be)

    def test_multiple_links(self):
        text = "This text contains [first link](https://example.com/first) and [second link](https://example.com/second)."
        result = extract_markdown_links(text)
        should_be = [
            ("first link", "https://example.com/first"),
            ("second link", "https://example.com/second")
        ]

        self.assertEqual(result, should_be)

    def test_no_links(self):
        text = "This text contains no links."
        result = extract_markdown_links(text)
        should_be = []

        self.assertEqual(result, should_be)

    def test_links_with_special_characters(self):
        text = "A link with special characters [special@link](https://example.com/link@name) and another [link&with*chars](https://example.com/link&name*)."
        result = extract_markdown_links(text)
        should_be = [
            ("special@link", "https://example.com/link@name"),
            ("link&with*chars", "https://example.com/link&name*")
        ]

        self.assertEqual(result, should_be)

    def test_link_with_spaces(self):
        text = "A link with spaces in the text [link with spaces](https://example.com)."
        result = extract_markdown_links(text)
        should_be = [("link with spaces", "https://example.com")]

        self.assertEqual(result, should_be)

    def test_multiple_lines(self):
        text = """
        This is text with multiple links:
        [first link](https://example.com/first)
        Some text in between.
        [second link](https://example.com/second)
        """
        result = extract_markdown_links(text)
        should_be = [
            ("first link", "https://example.com/first"),
            ("second link", "https://example.com/second")
        ]

        self.assertEqual(result, should_be)

class TestTextToTextNodes(unittest.TestCase):
    def test_mixed_formatting(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)

        should_be = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(result, should_be)

    def test_no_formatting(self):
        text = "This is plain text with no formatting."
        result = text_to_textnodes(text)

        should_be = [
            TextNode("This is plain text with no formatting.", TextType.TEXT)
        ]

        self.assertEqual(result, should_be)

    def test_only_bold(self):
        text = "This is **bold** text."
        result = text_to_textnodes(text)

        should_be = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT)
        ]

        self.assertEqual(result, should_be)

    def test_only_italic(self):
        text = "This is *italic* text."
        result = text_to_textnodes(text)

        should_be = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT)
        ]

        self.assertEqual(result, should_be)

    def test_only_code(self):
        text = "This is `code` text."
        result = text_to_textnodes(text)

        should_be = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.TEXT)
        ]

        self.assertEqual(result, should_be)

    def test_only_image(self):
        text = "This is an ![image](https://example.com/image.png)"
        result = text_to_textnodes(text)

        should_be = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png")
        ]

        self.assertEqual(result, should_be)

    def test_only_link(self):
        text = "This is a [link](https://example.com)"
        result = text_to_textnodes(text)

        should_be = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com")
        ]

        self.assertEqual(result, should_be)

    def test_combined_bold_italic(self):
        text = "This is **bold** and *italic* text."
        result = text_to_textnodes(text)

        should_be = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT)
        ]

        self.assertEqual(result, should_be)

if __name__ == "__main__":
    unittest.main()
