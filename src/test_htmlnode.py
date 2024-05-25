import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

class ParentNodeTest(unittest.TestCase):
    def test_basic_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        val = node.to_html()
        should_be = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(val, should_be)
    
    def test_no_children(self):
        node = ParentNode("p", [])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertTrue("ParentNode has no children" in str(context.exception))
    
    def test_no_tag(self):
        node = ParentNode(None, [LeafNode(None, "Text")])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertTrue("ParentNode is missing tag" in str(context.exception))
    
    def test_with_properties(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "Content")],
            props={"class": "container", "id": "main-div"}
        )
        val = node.to_html()
        should_be = '<div class="container" id="main-div">Content</div>'
        self.assertEqual(val, should_be)
    
    def test_nested_parent_node(self):
        node = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode(None, "Nested paragraph")]),
                LeafNode("span", "Some span")
            ]
        )
        val = node.to_html()
        should_be = '<div><p>Nested paragraph</p><span>Some span</span></div>'
        self.assertEqual(val, should_be)
    
    def test_various_tags(self):
        node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "Item 1")]),
                ParentNode("li", [LeafNode(None, "Item 2")]),
                ParentNode("li", [LeafNode(None, "Item 3")])
            ]
        )
        val = node.to_html()
        should_be = '<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>'
        self.assertEqual(val, should_be)

if __name__ == "__main__":
    unittest.main()
