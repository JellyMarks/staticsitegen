from enum import Enum
from markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown:str) -> list:
    split_markdown = markdown.split("\n")
    blocks = []
    current_block_lines = []

    for item in split_markdown:
        if item.strip() == "":
            if current_block_lines:
                new_block = "\n".join(current_block_lines)
                clean_block = new_block.strip()
                blocks.append(clean_block)
                current_block_lines = []
        else:
            current_block_lines.append(item)
    if current_block_lines:
        new_block = "\n".join(current_block_lines)
        clean_block = new_block.strip()
        blocks.append(clean_block)
        current_block_lines = []
    return blocks

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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    htmlnodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        hash_count = hash_count_helper(block)
        text = block_cleanup(block, block_type, hash_count)
        tag = block_type_to_tag(block_type, hash_count)

        if block_type == BlockType.CODE:
            code_nodes = []
            code_node = TextNode(text, TextType.CODE)
            c_node = text_node_to_html_node(code_node)
            code_nodes.append(c_node)
            new_node = ParentNode(tag="pre", children=code_nodes, props=None)
        elif block_type == BlockType.ORDERED_LIST or block_type == BlockType.UNORDERED_LIST:
            new_node = ParentNode(tag, text, props=None)
        else:
            new_node = ParentNode(tag, text_to_children(text), props=None)
            
        htmlnodes.append(new_node)
    finalnode = ParentNode(tag="div", children=htmlnodes, props=None)
    return finalnode


def block_type_to_tag(block_type, hash_count):
    if block_type == BlockType.PARAGRAPH:
        return "p"
    if block_type == BlockType.HEADING:
        return f"h{hash_count}"
    if block_type == BlockType.QUOTE:
        return "blockquote"
    if block_type == BlockType.UNORDERED_LIST:
        return "ul"
    if block_type == BlockType.ORDERED_LIST:
        return "ol"
    
def text_to_children(text):
    htmlnodes = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        htmlnodes.append(text_node_to_html_node(textnode))
    return htmlnodes

def block_cleanup(block, block_type, hash_count)-> str:
    cleaned_text = ()
    if block_type == BlockType.PARAGRAPH:
        split_text = block.split()
        
    if block_type == BlockType.HEADING:
        no_hash = block[hash_count:]
        joined_no_hash = "".join(no_hash)
        return joined_no_hash.strip()
            
    if block_type == BlockType.QUOTE:
        words = str(block)
        stripped = words.strip(">")
        split_text = stripped.split()

    if block_type == BlockType.UNORDERED_LIST:
        return list_cleanup(block, block_type)
            
    if block_type == BlockType.ORDERED_LIST:
        return list_cleanup(block, block_type)
    
    if block_type == BlockType.CODE:
        words = str(block)
        stripped = words.strip("```")
        split_text = stripped.split("\n")
        final_splits = []
        for bundle in split_text:
            final_splits.append(bundle.strip())
        final_splits.pop(0)
        cleaned_text = "\n".join(final_splits)
        return cleaned_text

    cleaned_text = " ".join(split_text)
    return cleaned_text

def list_cleanup(block, block_type) -> str:
    lines = block.split("\n")
    li_nodes = []
    
    for line in lines:
        if block_type == BlockType.UNORDERED_LIST:
            item_text = line[2:]

        if block_type == BlockType.ORDERED_LIST:
            period_index = line.find(". ")
            item_text = line[period_index + 2:]

        children = text_to_children(item_text)
        li_node = ParentNode("li", children, props=None)
        li_nodes.append(li_node)
    return li_nodes

def hash_count_helper(block):
    hash_count = 0
    for char in block:
        if char == "#":
            hash_count += 1
        else:
            break
    return hash_count