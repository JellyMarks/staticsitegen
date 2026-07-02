import unittest
from htmlnode import HTMLNode, LeafNode

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
    
    def test_leaf_to_html_not_value(self):
        node = LeafNode("a")
        self.assertEqual(node.to_html(), ValueError)

if __name__ == "__main__":
    unittest.main()