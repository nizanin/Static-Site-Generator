

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props:
            return " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())
        return ""
    
    def __repr__(self):
        return (
            f"HTMLNode("
            f"tag={repr(self.tag)}, "
            f"value={repr(self.value)}, "
            f"children={repr(self.children)}, "
            f"props={repr(self.props)}"
            f")"
        )
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        if value is None:
            raise ValueError("LeafNode must have a value")

        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError ("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return (
            f"HTMLNode("
            f"tag={repr(self.tag)}, "
            f"value={repr(self.value)}, "
            f"props={repr(self.props)}"
            f")"
        )
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children,  props = None):
        if not children or not isinstance(children, list):
            raise ValueError("ParentNode must have a non-empty list of children")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have a children")
        children_html = "".join(child.to_html() for child in self.children)
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'