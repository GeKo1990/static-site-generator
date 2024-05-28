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

def markdown_to_blocks(markdown):
    # Split the markdown text into blocks using double newlines
    blocks = markdown.split('\n\n')
    
    clean_blocks = []
    
    for block in blocks:
        # Further split blocks by single newlines if they contain list items
        sub_blocks = block.split('\n')
        for sub_block in sub_blocks:
            clean_sub_block = sub_block.strip()
            if clean_sub_block:
                clean_blocks.append(clean_sub_block)
    
    return clean_blocks

main()