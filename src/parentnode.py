from typing import List, Dict, Optional

from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, 
                 tag: str | None = None, 
                 children: List[HTMLNode] | None = None, 
                 props: Dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode is missing tag")
        elif len(self.children) < 1:
            raise ValueError("ParentNode has no children")
        
        children_html = ''.join(child.to_html() for child in self.children)
        props_html = ''
        if self.props:
            props_html = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
            props_html = ' ' + props_html

        return f'<{self.tag}{props_html}>{children_html}</{self.tag}>'

        
