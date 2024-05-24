from textnode import TextNode
from htmlnode import HTMLNode, LeafNode

def main():
    print("hello world")

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node == None:
        raise ValueError("No TextNode provided")
    if text_node.text_type not in supported_text_types():
        raise ValueError(f'{text_node.text_type} is not supported')
    
    type = text_node.text_type
    if type == "text_type_text":
        return LeafNode(None, text_node.text)
        
    
def supported_text_types() -> dict:
    return {
        "text_type_text" : "text",
        "text_type_bold" : "bold",
        "text_type_italic" : "italic",
        "text_type_code" : "code",
        "text_type_link" : "link",
        "text_type_image" : "image"
    }

main()