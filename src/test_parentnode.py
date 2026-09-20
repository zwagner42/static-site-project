import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestTextNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_properties_simple(self):
        child_node = LeafNode("span", "child", {"style": "color: red"})
        parent_node = ParentNode("div", [child_node], {"class": "test_class"})
        self.assertEqual(parent_node.to_html(), "<div class='test_class'><span style='color: red'>child</span></div>")

if __name__ == "__main__":
    unittest.main()
