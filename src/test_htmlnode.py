import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("h1", "This is a test", None, {"href": "https://www.google.com", "target": "_blank"})
        should_be = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), should_be)

    def test_props_to_html_empty_props(self):
        node = HTMLNode("p", "This is a paragraph", None, {})
        should_be = ''
        self.assertEqual(node.props_to_html(), should_be)
        
    def test_props_to_html_multiple_props(self):
        node = HTMLNode("a", "Click here", None, {"href": "https://www.example.com", "title": "Example", "class": "example-link"})
        should_be = 'href="https://www.example.com" title="Example" class="example-link"'
        self.assertEqual(node.props_to_html(), should_be)

if __name__ == "__main__":
    unittest.main()
