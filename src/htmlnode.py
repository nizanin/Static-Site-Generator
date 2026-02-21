

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
            return " ".join(f'{k}="{v}"' for k, v in self.props.items())
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