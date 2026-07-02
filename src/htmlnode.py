class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        #A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.tag = tag
        #A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.value = value
        #A list of HTMLNode objects representing the children of this node
        self.children = children
        #A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None or self.props == "":
            return ""
        result = []
        for key, value in self.props.items():
            value = str(value)
            result.append(f' {key}="{value}"')
        return "".join(result)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)

    def to_html(self):
        if not self.value:
            raise ValueError
        elif not self.tag:
            return str(self.value)
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"