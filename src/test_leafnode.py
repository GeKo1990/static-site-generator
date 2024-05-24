import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag_and_value(self):
        node = LeafNode("h1", "This is a test")
        val = node.to_html()
        should_be = "<h1>This is a test</h1>"
        self.assertEqual(val, should_be)

    def test_to_html_with_tag_and_value_bold(self):
        node = LeafNode("b", "Bold Text")
        val = node.to_html()
        should_be = "<b>Bold Text</b>"
        self.assertEqual(val, should_be)

    def test_to_html_with_tag_and_value_italic(self):
        node = LeafNode("i", "Italic Text")
        val = node.to_html()
        should_be = "<i>Italic Text</i>"
        self.assertEqual(val, should_be)

    def test_to_html_with_value_only(self):
        node = LeafNode(value="Plain Text")
        val = node.to_html()
        should_be = "Plain Text"
        self.assertEqual(val, should_be)

    def test_to_html_with_tag_only(self):
        node = LeafNode(tag="h1")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_img_tag(self):
        node = LeafNode(tag='img', props={'src': 'image.png', 'alt': 'An image'})
        val = node.to_html()
        should_be = '<img src="image.png" alt="An image"/>'
        self.assertEqual(val, should_be)

    def test_to_html_with_a_tag(self):
        node = LeafNode(tag='a', value='Google', props={'href': 'https://www.google.com', 'target': '_blank'})
        val = node.to_html()
        should_be = '<a href="https://www.google.com" target="_blank">Google</a>'
        self.assertEqual(val, should_be)

if __name__ == "__main__":
    unittest.main()
