import re

from typing import List, Union, Optional

from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: Union[str, TextType], url: Optional[str] = None):
        self.text = text
        if isinstance(text_type, TextType):
            self.text_type = text_type.value
        else:
            self.text_type = text_type
        self.url = url

    def __eq__(self, value: object) -> bool:
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
    
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
    
def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
        
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, 'text'))
            else:
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes

def extract_markdown_images(text: str) -> list:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text: str) -> list:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


    
