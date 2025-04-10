class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # Handle opening tag
        props_html = self.props_to_html()
        opening = f"<{self.tag}{props_html}>"

        # Handle value or render children if present
        body = ""
        if self.value:  # If value exists, use it as the body's content
            body = self.value
        elif self.children:  # If children exist, recursively build their HTML
            for child in self.children:
                body += child.to_html()

        # Handle closing tag
        closing = f"</{self.tag}>"

        # Combine everything together
        return f"{opening}{body}{closing}"

    def props_to_html(self):
        if self.props is None:
            return ""
        props_to_html = ""
        for prop in self.props:
            props_to_html += f' {prop}="{self.props[prop]}"'
        return props_to_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children:{self.children}, {self.props})"


class LeafNode(HTMLNode):
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


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")
        # Otherwise using recursion concentnate the HTML node and its children
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
