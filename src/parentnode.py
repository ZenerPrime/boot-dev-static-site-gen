from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag = tag, props = props, children = children)

    def to_html(self):
        if (self.tag == None):
            raise ValueError("ParentNode must have a tag")
        if (not self.children):
            raise ValueError("ParentNode must have children")
        return f"<{self.tag}{self.props_to_html()}>{"".join(map(lambda c: c.to_html(), self.children))}</{self.tag}>"
