from htmlnode import HTMLNode


class ParentNode(HTMLNode):

    def __init__(self, tag: str | None, children: list['HTMLNode'] | None, props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode has no tag")

        if not self.children:
            raise ValueError("ParentNode has no children")

        full_output = f"<{self.tag}"

        if self.props:
            for key in self.props:
                full_output += f" {key}='{self.props[key]}'"

        full_output += ">"

        for child in self.children:
            full_output += child.to_html()

        full_output += f"</{self.tag}>"

        return full_output
