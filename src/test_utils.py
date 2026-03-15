import unittest
from utils import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_basic_title(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    def test_title_with_spaces(self):
        md = "#    My Title   "
        self.assertEqual(extract_title(md), "My Title")

    def test_no_h1(self):
        md = "## Subtitle\nSome text"
        with self.assertRaises(ValueError):
            extract_title(md)



if __name__ == "__main__":
    unittest.main()