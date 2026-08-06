import unittest
from main import extract_title


class TestExtract_Title(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Test Title"
        test = extract_title(markdown)
        self.assertEqual(test, 'Test Title')

    def test_extract_title_not_h1(self):
            markdown = "### Test Subheading"
            with self.assertRaises(Exception):
                extract_title(markdown)

    def test_extract_title_title(self):
                markdown = "Test non-heading"
                with self.assertRaises(Exception):
                    extract_title(markdown)

    def test_extract_title_weird_heading(self):
            markdown = "# #Test Weird Title"
            test = extract_title(markdown)
            self.assertEqual(test, '#Test Weird Title')