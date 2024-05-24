import unittest

from htmlnode import LeafNode, ParentNode

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


