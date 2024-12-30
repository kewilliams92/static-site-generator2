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


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        # Ensuring props is a dictionary
        if self.props is None:
            self.props = {}
        elif not isinstance(self.props, dict):
            raise TypeError(
                f"Props must be a dictionary, but got {type(self.props)} instead"
            )
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
