import unittest

from markdown_helpers import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks
)

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_split_delimiter_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "code block")

    def test_split_delimiter_bold(self):
        node = TextNode("Now this is some text with **bold text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "bold text")

    def test_split_delimiter_italic(self):
        node = TextNode("Now this is some text with _italic text_, dang", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "italic text")

    def test_split_delimiter_few_nodes(self):
        node1 = TextNode("Now this is some text with _italic text_ and some **bold text**, dang", TextType.TEXT)
        node2 = TextNode("This is text with **a** `code block` word", TextType.TEXT)
        node3 = TextNode("Now this is some text with **bold text**", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 9)
        self.assertEqual(new_nodes[1].text, "bold text")
        self.assertEqual(new_nodes[4].text, "a")
        self.assertEqual(new_nodes[7].text, "bold text")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link to click](www.google.com)"
        )
        self.assertListEqual([("link to click", "www.google.com")], matches)

    def test_extract_markdown_images_more(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). This is a ![second image to deal with](https://i.imgur.com/zjjcJKZ.png), and your going to like it. asodifjasodif ja [  aoisdjfoa isjdf [  asdf[]  9)   asdfjaosdifj ()"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("second image to deal with", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_more(self):
        matches = extract_markdown_links(
            "This is text with an [link to click](www.google.com). aodifjoi aod fjafao sd aod fojaowefnw eoifn [ ajdsiofp p ] padsfjoad[d [] [link here](www.google.com)fsdafi dajfisdfoaisdjfo idfjdi"
        )
        self.assertListEqual([("link to click", "www.google.com"), ("link here", "www.google.com")], matches)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_in_middle(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes
        )

    def test_split_links_in_middle(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and that's all",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and that's all", TextType.TEXT),
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    #TODO Write more test for test_text_to_textnodes, markdown_to_blocks

if __name__ == "__main__":
    unittest.main()
