import re

from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode
from leafnode import LeafNode
from src.parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


def text_to_textnodes(text: str) -> list[TextNode]:
    if not text:
        return []

    starting_node = TextNode(text, TextType.TEXT, None)
    result = split_nodes_delimiter([starting_node], "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_link(result)

    return result

def markdown_to_blocks(markdown: str) -> list[str]:
    if not markdown:
        return []

    blocks = [block.strip() for block in markdown.split("\n\n") if block]

    return blocks


def markdown_to_html_node(markdown: str) -> HTMLNode:
    if not markdown:
        return HTMLNode(None, None, None, None)

    markdown_blocks = markdown_to_blocks(markdown)

    children = []
    for block in markdown_blocks:
        new_node = block_to_html_node(block)
        children.append(new_node)

    return ParentNode("div", children)


def block_to_html_node(block) -> ParentNode:
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            return block_to_paragraph(block)
        case BlockType.QUOTE:
            return block_to_blockquote(block)
        case BlockType.UNORDERED_LIST:
            return block_to_unordered_list(block)
        case BlockType.ORDERED_LIST:
            return block_to_ordered_list(block)
        case BlockType.CODE:
            return block_to_code(block)
        case BlockType.HEADING:
            return block_to_heading(block)

def block_to_paragraph(block: str) -> ParentNode:
    parent = ParentNode("p", [])

    parent.children = text_to_children(block.replace("\n", " "))

    return parent

def block_to_blockquote(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []

    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")

        new_lines.append(line.lstrip(">").strip())

    content = " ".join(new_lines)
    children = text_to_children(content)

    return ParentNode("blockquote", children)

def block_to_unordered_list(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for list_item in items:
        text = list_item[2:]
        html_items.append(ParentNode("li", text_to_children(text)))

    return ParentNode("ul", html_items)

def block_to_ordered_list(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for list_item in items:
        parts = list_item.split(". ", 1)
        text =parts[1]
        html_items.append(ParentNode("li", text_to_children(text)))

    return ParentNode("ol", html_items)

def block_to_code(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")

    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    code = ParentNode("code", [text_node_to_html_node(raw_text_node)])

    return ParentNode("pre", [code])

def block_to_heading(block: str) -> ParentNode:
    num_signs = 0
    for index in range(len(block)):
        if block[index] != "#":
            break
        num_signs += 1

    if num_signs + 1 > 6:
        raise ValueError(f"invalid heading level: {num_signs}")

    return ParentNode(f"h{num_signs}", text_to_children(block[num_signs + 1:]))

def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:

    new_nodes = []

    for old_node in old_nodes:
        if old_node.text == "":
            continue
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_content = old_node.text.split(delimiter)

        if len(split_content) % 2 == 0:
            raise Exception("Delimiter exist without a closing delimiter")

        for i in range(len(split_content)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_content[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_content[i], text_type))

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text == "":
            continue
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        build_nodes_text = old_node.text
        for image in images:
            split_text = build_nodes_text.split(f"![{image[0]}]({image[1]})")
            new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            if len(split_text) > 1:
                build_nodes_text = "".join(split_text[1:])

        if build_nodes_text != "":
            new_nodes.append(TextNode(build_nodes_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text == "":
            continue
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        build_nodes_text = old_node.text
        for link in links:
            split_text = build_nodes_text.split(f"[{link[0]}]({link[1]})")
            new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            if len(split_text) > 1:
                build_nodes_text = "".join(split_text[1:])

        if build_nodes_text != "":
            new_nodes.append(TextNode(build_nodes_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text: str):
    if not text:
        return []

    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_regex, text)

    return matches

def extract_markdown_links(text: str):
    if not text:
        return []

    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_regex, text)

    return matches
