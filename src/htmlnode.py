
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if children is None:
            children = []
        if props is None:
            props = {}

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props != None:
            HTML_string = ""
            for key, value in self.props.items():
                HTML_string += " " + key + '="' + value + '"'
            return HTML_string
        return ""
        
    def __repr__(self):
        return f"HTMLNode(tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props=props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag is required")
        if self.children == None:
            raise ValueError("Children is required")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"