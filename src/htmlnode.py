class HTMLNode:

    def __init__(self, tag: str | None=None, value: str | None=None,
        children: list['HTMLNode'] | None=None, props: dict[str, str] | None=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""

        html = ""
        for key in self.props:
            html += f" {key}={self.props[key]}"

        return html

    def __repr__(self):
        full_output = ""

        full_output += f"Tag: {self.tag}\n"
        full_output += f"Value: {self.value}\n"
        full_output += f"Children: {self.children}\n"
        full_output += f"Props: {self.props}\n"

        return full_output
