from textnode import text_node_to_html_node, text_to_textnodes
from htmlnode import ParentNode

import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

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
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def unordered_list_to_html_node(block):
    list_items = block.split("\n")
    html_items = []
    for item in list_items:
        match = re.match(r"^[\*-] (.*)", item)
        if not match:
            raise ValueError('invalid unordered list item')
        text = match.group(1)
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def ordered_list_to_html_node(block):
    list_items = block.split("\n")
    html_items = []
    for item in list_items:
        match = re.match(r"^\d+\. (.*)", item)
        if not match:
            raise ValueError('invalid ordered list item')
        text = match.group(1)
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def code_to_html_node(block):
    match = re.match(r"^```(.*?*)```$", block, re.DOTALL)
    if not match:
        raise ValueError('invalid code block')
    
    text = match.group(1)
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def heading_to_html_node(block):
    match = re.match(r"^(#{1,6}) (.+)$", block)
    if not match:
        raise ValueError('Invalid heading format')
    
    level = len(match.group(1))
    text = match.group(2)
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def quote_to_html_node(block):
    matches = re.findall(r"^> (.*)", block, re.MULTILINE)
    if not matches:
        raise ValueError("Invalid quote block")
    
    content = " ".join(matches)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


