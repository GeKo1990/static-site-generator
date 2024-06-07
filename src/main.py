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

import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

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

def block_to_block_type(block):
    if re.match(r"^[1-6]# ", block):
        return block_type_heading
    elif re.match(r"^```.*```$", block, re.DOTALL):
        return block_type_code
    elif all(re.match(r"^>", line) for line in block.split('\n')):
        return block_type_quote
    elif all(re.match(r"^[\*-] ", line) for line in block.split('\n')):
        return block_type_unordered_list
    elif all(re.match(r"^\d+\. ", line) for line in block.split('\n')):
        return block_type_ordered_list
    else:
        return block_type_paragraph

main()