import re

from textnode import TextNode, TextType


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

    blocks = [block.strip() for block in markdown.split("\n\n")]

    return blocks


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:

    new_nodes = []
    delimiter_text_type = TextType.TEXT

    match delimiter:
        case "**":
            delimiter_text_type = TextType.BOLD
        case "_":
            delimiter_text_type = TextType.ITALIC
        case "`":
            delimiter_text_type = TextType.CODE
        case _:
            delimiter_text_type = TextType.TEXT

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
                new_nodes.append(TextNode(split_content[i], delimiter_text_type))

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
