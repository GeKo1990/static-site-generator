import unittest

from main import markdown_to_blocks

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

if __name__ == '__main__':
    unittest.main()
