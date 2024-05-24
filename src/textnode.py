class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object) -> bool:
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
    
    def __supported_types(self) -> dict:
        return {
            "text_type_text" : "text",
            "text_type_bold" : "bold",
            "text_type_italic" : "italic",
            "text_type_code" : "code",
            "text_type_link" : "link",
            "text_type_image" : "image"
        }