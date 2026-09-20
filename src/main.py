from textnode import TextNode, TextType


def main():
    textNode = TextNode("This is some anchor text", TextType.LINK, "https://www.bootdev")
    print(textNode)

main()
