from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
    print("hello world")

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node is None:
        raise ValueError("No TextNode provided")
    
    if text_node.text_type == TextType.TEXT.value:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD.value:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC.value:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE.value:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK.value:
        return LeafNode("a", text_node.text, { "href" : text_node.url })
    elif text_node.text_type == TextType.IMAGE.value:
        return LeafNode("img","", { "src" : text_node.url, "alt" : text_node.text })
    else:
        raise ValueError(f'{text_node.text_type} is not supported')
        

main()