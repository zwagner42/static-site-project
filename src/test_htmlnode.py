import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_node_repr(self):
        children = [HTMLNode(None, None, None, None)]
        props = {
            "href": "www.google.com",
            "target": "_blank"
        }
        node = HTMLNode("a", "This is some inner text", children, props)

        printed_output = repr(node)

        if printed_output:
            self.assertIn("Tag: ", printed_output)
            self.assertIn("Value: ", printed_output)
            self.assertIn("Children: ", printed_output)
            self.assertIn("Props: ", printed_output)
        else:
            self.fail("Test was self failed due to printed_output being None")


    def test_props_to_html(self):
        props = {
            "href": "www.google.com",
            "target": "_blank"
        }
        node = HTMLNode("a", "This is some inner text", None, props)
        full_props = node.props_to_html()
        self.assertIn("href=", full_props)
        self.assertIn("target=", full_props)

    def test_node_none(self):
        node = HTMLNode(None, None, None, None)

        printed_output = repr(node)

        if printed_output:
            self.assertIn("Tag: None", printed_output)
            self.assertIn("Value: None", printed_output)
            self.assertIn("Children: None", printed_output)
            self.assertIn("Props: None", printed_output)
        else:
            self.fail("Test was self failed due to printed_output being None")

if __name__ == "__main__":
    unittest.main()
