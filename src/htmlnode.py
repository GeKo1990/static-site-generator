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
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        if not self.props:
            return ''
        return ' '.join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
    

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
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

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
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"