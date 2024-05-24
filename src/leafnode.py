from typing import List, Dict, Optional

from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, 
                 tag: Optional[str] = None, 
                 value: Optional[str] = None, 
                 props: Optional[Dict[str, str]] = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None and self.tag != "img":
            raise ValueError
    
        if self.tag == None:
            return self.value
        
        return self.__wrap_with_tag()
        
    def __wrap_with_tag(self):
        if self.tag == 'img':
            return f'<{self.tag} {super().props_to_html()}/>'
        elif len(self.props) > 0:
            return f'<{self.tag} {super().props_to_html()}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag}>{self.value}</{self.tag}>'
