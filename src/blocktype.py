import re
from enum import Enum

HEADING_REGEX = r"^#{1,6}\s[\s\S]*"
CODE_REGEX = r"^`{3}\n[\s\S]+`{3}$"
QUOTE_REGEX = r"(?:^>[^\n]*\n*)+"
UNORDERED_LIST_REGEX = r"(?:^-\s[^\n]*\n*)+"
ORDERED_LIST_REGEX = r"^\d+\.\s.*$"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown_block: str) -> BlockType:

    if len(re.findall(HEADING_REGEX, markdown_block)) > 0:
        return BlockType.HEADING
    elif len(re.findall(CODE_REGEX, markdown_block)) > 0:
        return BlockType.CODE
    elif len(re.findall(QUOTE_REGEX, markdown_block, re.MULTILINE)) > 0:
        return BlockType.QUOTE
    elif len(re.findall(UNORDERED_LIST_REGEX, markdown_block, re.MULTILINE)) > 0:
        return BlockType.UNORDERED_LIST
    else:
        matches = re.findall(ORDERED_LIST_REGEX, markdown_block, re.MULTILINE)

        if len(matches) != 0:

            for i in range(len(matches)):
                if i + 1 != int(matches[i][0]):
                    return BlockType.PARAGRAPH

            return BlockType.ORDERED_LIST



    return BlockType.PARAGRAPH
