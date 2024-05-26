from textnode import TextNode, TextType, split_nodes_delimiter
from htmlnode import LeafNode

def main():
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    for n in new_nodes:
        print(n)

main()