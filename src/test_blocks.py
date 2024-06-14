import unittest
import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import (
    markdown_to_blocks,
    block_to_block_type,
    paragraph_to_html_node,
    heading_to_html_node,
    unordered_list_to_html_node,
    ordered_list_to_html_node,
    code_to_html_node,
    quote_to_html_node,
    block_to_html_node,
    markdown_to_html_node
)

class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_markdown_to_html_node(self):
        markdown = """
        # Heading 1

        This is a paragraph with some **bold** and *italic* text.

        * List item 1
        * List item 2

        1. Ordered item 1
        2. Ordered item 2

        ```
        print('Hello, world!')
        ```

        > This is a quote
        """

        expected_output = "<div><h1>Heading 1</h1><p>This is a paragraph with some <b>bold</b> and <i>italic</i> text.</p><p><i> List item 1         </i> List item 2</p><p>1. Ordered item 1         2. Ordered item 2</p><pre><code>print('Hello, world!')</code></pre><blockquote>This is a quote</blockquote></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_output)

    def test_empty_markdown(self):
        markdown = ""
        expected_output = ParentNode("div", [])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_basic_markdown(self):
        raw_markdown = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is a list item
        * This is another list item
        """
        expected_output = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n        * This is another list item"
        ]
        self.assertEqual(markdown_to_blocks(raw_markdown), expected_output)
    
    def test_empty_markdown(self):
        raw_markdown = ""
        expected_output = []
        self.assertEqual(markdown_to_blocks(raw_markdown), expected_output)
    
    def test_markdown_with_extra_spaces(self):
        raw_markdown = """
        # This is a heading  

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.  

        * This is a list item
        * This is another list item
        """
        expected_output = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n        * This is another list item"
        ]
        self.assertEqual(markdown_to_blocks(raw_markdown), expected_output)
    
    def test_markdown_with_single_line(self):
        raw_markdown = "# This is a single line of markdown"
        expected_output = ["# This is a single line of markdown"]
        self.assertEqual(markdown_to_blocks(raw_markdown), expected_output)

    def test_markdown_with_multiple_blank_lines(self):
        raw_markdown = """
        This is a paragraph


        Another paragraph with multiple blank lines


        End of markdown
        """
        expected_output = [
            "This is a paragraph",
            "Another paragraph with multiple blank lines",
            "End of markdown"
        ]
        self.assertEqual(markdown_to_blocks(raw_markdown), expected_output)

class TestBlockToBlockType(unittest.TestCase):
    def test_block_type_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_block_type_code(self):
        block = "```code block```"
        self.assertEqual(block_to_block_type(block), "code")
    
    def test_block_type_quote(self):
        block = "> Quote line 1\n> Quote line 2"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_block_type_unordered_list(self):
        block = "* Unordered list item 1\n* Unordered list item 2"
        self.assertEqual(block_to_block_type(block), "unordered_list")

        block = "- Unordered list item 1\n- Unordered list item 2"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_type_ordered_list(self):
        block = "1. Ordered list item 1\n2. Ordered list item 2"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_block_type_paragraph(self):
        block = "This is a regular paragraph without any special formatting."
        self.assertEqual(block_to_block_type(block), "paragraph")

class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraph_to_html_node(self):
        block = "This is a paragraph with multiple lines.\nIt should be joined into one line."
        expected_output = ParentNode("p", [LeafNode(value="This is a paragraph with multiple lines. It should be joined into one line.")])
        self.assertEqual(paragraph_to_html_node(block), expected_output)

    def test_unordered_list_to_html_node(self):
        block = "* Item 1\n* Item 2\n- Item 3"
        expected_output = ParentNode("ul", [
            ParentNode("li", [LeafNode(value="Item 1")]),
            ParentNode("li", [LeafNode(value="Item 2")]),
            ParentNode("li", [LeafNode(value="Item 3")])
        ])
        self.assertEqual(unordered_list_to_html_node(block), expected_output)

    def test_ordered_list_to_html_node(self):
        block = "1. First item\n2. Second item"
        expected_output = ParentNode("ol", [
            ParentNode("li", [LeafNode(value="First item")]),
            ParentNode("li", [LeafNode(value="Second item")])
        ])
        self.assertEqual(ordered_list_to_html_node(block), expected_output)

    def test_code_to_html_node(self):
        block = "```print('Hello, world!')```"
        expected_output = ParentNode("pre", [
            ParentNode("code", [LeafNode(value="print('Hello, world!')")])
        ])
        self.assertEqual(code_to_html_node(block), expected_output)

    def test_heading_to_html_node(self):
        block = "### This is a heading"
        expected_output = ParentNode("h3", [LeafNode(value="This is a heading")])
        self.assertEqual(heading_to_html_node(block), expected_output)

    def test_quote_to_html_node(self):
        block = "> Quote line 1\n> Quote line 2"
        expected_output = ParentNode("blockquote", [LeafNode(value="Quote line 1 Quote line 2")])
        self.assertEqual(quote_to_html_node(block), expected_output)

if __name__ == '__main__':
    unittest.main()
