from htmlnode import HTMLNode


class LeafNode(HTMLNode):

    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("No value stored in this LeafNode")

        if not self.tag:
            return self.value


        props_text = ""
        if self.props:
            for key in self.props:
                props_text += f" {key}='{self.props[key]}'"

        return f"<{self.tag}{props_text}>{self.value}</{self.tag}>"


    def __repr__(self):
        full_output = ""

        full_output += f"Tag: {self.tag}\n"
        full_output += f"Value: {self.value}\n"
        full_output += f"Props: {self.props}\n"

        return full_output
