import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_invalid_texttype(self):
        with self.assertRaises(ValueError):
            TextNode("This is invalid text node", "TextType.Invalid", "http://google.com")
        with self.assertRaises(AttributeError):
            TextNode("This is invalid text node", TextType.Invalid, "http://google.com")

    def test_urlIsNone(self):
        node1 = TextNode("text", TextType.LINK, "")
        node2 = TextNode("text", TextType.LINK, " ")
        self.assertNotEqual(node1, node2)
    
    def test_missingUrlException(self):
        with self.assertRaises(Exception):
            TextNode("No URL testcase", TextType.LINK)




if __name__ == "__main__":
    unittest.main()