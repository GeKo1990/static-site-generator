from htmlnode import LeafNode
from textnode import (
    TextNode, 
    TextType, 
    text_node_to_html_node,
    text_to_textnodes,
    split_nodes_delimiter, 
    extract_markdown_links, 
    extract_markdown_images, 
    split_nodes_link, 
    split_nodes_image
)

def main():
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        print(result)

main()