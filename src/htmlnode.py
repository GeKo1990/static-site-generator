from typing import List, Dict, Optional

class HTMLNode:
    def __init__(self, 
                 tag: Optional[str] = None, 
                 value: Optional[str] = None, 
                 children: Optional[List['HTMLNode']] = None, 
                 props: Optional[Dict[str, str]] = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

        if self.tag is None and self.value is None and not self.children:
            # If no tag, value, and children, default to empty string for value
            self.value = ''
        elif self.tag is not None and self.value is None and not self.children:
            # If there's a tag but no value or children, default to empty string for value
            self.value = ''
        elif self.tag is not None and self.children is None:
            # If there's a tag and value, but no children, default children to empty list
            self.children = []
        elif self.tag is None and self.value is not None and self.children:
            # If there's no tag, but value and children are given, ignore the children
            self.children = []
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        if not self.props:
            return ''
        return ' '.join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'