import unittest

from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        props = {
            "href": "www.google.com",
            "target": "_blank"
        }
        node = LeafNode("a", "This is a link!", props)
        self.assertEqual(node.to_html(), "<a href='www.google.com' target='_blank'>This is a link!</a>")

    def test_leaf_repr(self):
        props = {
            "href": "www.google.com",
            "target": "_blank"
        }
        node = LeafNode("a", "This is some inner text", props)

        printed_output = repr(node)

        if printed_output:
            self.assertIn("Tag: ", printed_output)
            self.assertIn("Value: ", printed_output)
            self.assertIn("Props: ", printed_output)
        else:
            self.fail("Test was self failed due to printed_output being None")

if __name__ == "__main__":
    unittest.main()
