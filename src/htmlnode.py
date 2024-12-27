class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_to_html = ""
        for prop in self.props:
            props_to_html += f' {prop}="{self.props[prop]}"'
        return props_to_html

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, children:{self.children}, {self.props})"