from textnode import TextNode
from htmlnode import HTMLNode

def main():
    test = TextNode("This is a text node", "bold", "https://www.boot.dev")
    node = HTMLNode("h1", "This is a test", None, {"href": "https://www.google.com", "target": "_blank"})
    print(test)
    print(node)
    print(node.props_to_html())

main()