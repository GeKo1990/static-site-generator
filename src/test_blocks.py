import unittest

from blocks import markdown_to_blocks, block_to_block_type

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
            "* This is a list item",
            "* This is another list item"
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
            "* This is a list item",
            "* This is another list item"
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
        block = "1# This is a heading"
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

if __name__ == '__main__':
    unittest.main()
