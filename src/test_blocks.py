import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

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

    #MARKDOWN TO NODE TESTS

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
This is an unordered list with
    
- multiple lines
- unorganized text
- no numbers

This is an organized list with
    
1. multiple lines
2. organized text
3. all numbers
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is an unordered list with</p><ul><li>multiple lines</li><li>unorganized text</li><li>no numbers</li></ul><p>This is an organized list with</p><ol><li>multiple lines</li><li>organized text</li><li>all numbers</li></ol></div>",
        )

    def test_markdown_to_blocks_test_lists(self):
        md = """
This is an unordered list with
    
- multiple lines
- unorganized text
- no numbers

This is an organized list with
    
1. multiple lines
2. organized text
3. all numbers
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is an unordered list with",
                "- multiple lines\n- unorganized text\n- no numbers",
                "This is an organized list with",
                "1. multiple lines\n2. organized text\n3. all numbers",
            ],
        )

    def test_headingblock(self):
        md = """
# Heading here

###### Heading here

### Heading here
"""
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading here</h1><h6>Heading here</h6><h3>Heading here</h3></div>",
        )

if __name__ == "__main__":
    unittest.main()