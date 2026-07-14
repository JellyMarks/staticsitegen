import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestBlocks(unittest.TestCase):

    #MD TO BLOCK TESTS

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

    def test_markdown_to_blocks_empty(self):
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

    def test_markdown_to_blocks_whitespace_check(self):
        md = "First block\n\n   \n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
            ],
        )

    #BLOCK TO BLOCK TESTS

    def test_block_to_block_type_code(self):
        md = "```\nThis is a code block\n```"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.CODE
        )

    def test_block_to_block_type_bad_code(self):
        md = "```\nThis is a code block"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_quote(self):
        md = "> 'This is a famous quote block'"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.QUOTE
        )

    def test_block_to_block_type_bad_quote(self):
        md = "> line one\nline two"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_unordered_list(self):
        md = "- This is a list\n- with items"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_bad_unordered_list(self):
        md = "- This is a list\n+ with items"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_paragraph(self):
        md = "This is a normal paragraph"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_heading(self):
        md = "###### THIS IS A HEADING"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.HEADING
        )

    def test_block_to_block_type_long_heading(self):
        md = "####### THIS IS A BAD HEADING"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_bad_heading(self):
        md = "#Not a heading"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_ordered_list(self):
        md = "1. This is an ordered list\n2. with ordered items"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_bad_ordered_list(self):
        md = "1. This is an ordered list\n4. with unordered items"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_worse_ordered_list(self):
        md = "2. nope\n3. nope"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.PARAGRAPH
        )

if __name__ == "__main__":
    unittest.main()