import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_prop_to_html(self):
        node = HTMLNode(props={"test": "https://www.test.com", "nottest": "https://www.nottest.com"})
        test = node.props_to_html()
        self.assertEqual(test, ' test="https://www.test.com" nottest="https://www.nottest.com"')
    
    def test_prop_to_html_empty(self):
        node = HTMLNode(props={})
        test = node.props_to_html()
        self.assertEqual(test, "")

    def test_prop_to_html_none(self):
        node = HTMLNode(props=None)
        test = node.props_to_html()
        self.assertEqual(test, "")

    def test__repr__(self):
        node = HTMLNode("test", "abcd", children=None, props=None)
        test = node.__repr__()
        self.assertEqual(test, "HTMLNode(test, abcd, None, None)")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("p", "Hello, world!", props={"test": "https://www.test.com"})
        self.assertEqual(node.to_html(), '<p test="https://www.test.com">Hello, world!</p>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_prop_to_html(self):
        node = LeafNode("a", "Test Deez!", props={"test": "https://www.test.com", "nottest": "https://www.nottest.com"})
        self.assertEqual(node.to_html(), '<a test="https://www.test.com" nottest="https://www.nottest.com">Test Deez!</a>')

class TestParentNode(unittest.TestCase):
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

    def test_to_html_no_tag(self):
        parent_node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_with_multiple_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, "Normal"),
                LeafNode("i", "Italic"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold</b>Normal<i>Italic</i></p>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )

    def test_to_html_deeply_nested(self):
        great_grandchild = LeafNode("i", "deep text")
        grandchild = ParentNode("span", [great_grandchild])
        child = ParentNode("div", [grandchild])
        parent = ParentNode("section", [child])
        self.assertEqual(
            parent.to_html(),
            "<section><div><span><i>deep text</i></span></div></section>",
        )

    def test_to_html_mixed_children(self):
        parent_node = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode("b", "bold paragraph")]),
                LeafNode(None, "plain text"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><p><b>bold paragraph</b></p>plain text</div>",
        )

if __name__ == "__main__":
    unittest.main()