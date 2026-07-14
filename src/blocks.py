from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown:str) -> list:
    split_markdown = markdown.split("\n\n")
    block = []
    for item in split_markdown:
        stripped_item = item.strip()
        if stripped_item == "":
            continue
        block.append(stripped_item)
    return block

def block_to_block_type(block:str) -> BlockType:
    if block.startswith("#"):
        hash_count = 0
        for char in block:
            if char == "#":
                hash_count += 1
            else:
                break
        if 1 <= hash_count <= 6 and len(block) > hash_count and block[hash_count] == " ":
            return BlockType.HEADING
        
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    expected = 1

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    for line in lines:
        prefix = f"{expected}. "
        if line.startswith(prefix):
            expected += 1
        else:
            return BlockType.PARAGRAPH
    return BlockType.ORDERED_LIST