import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from main import text_node_to_html_node
from textnode import *
from blocktypes import extract_title

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="b", value="BOLD TEXT")
        expected_result = 'HTMLNode(tag:b, value:BOLD TEXT, children:[], props:{})'
        self.assertEqual(str(node), expected_result)

    def test_props_to_html(self):
        prop_case = {
            "href": "https://www.google.com",
            "target": "_blank",
            }
        expected_result =  ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(tag="b", value="link", children=None, props=prop_case)
        self.assertEqual(repr(str(node.props_to_html())), repr(expected_result))
        
        prop_case2 ={
            "href": "https://www.google.com",
            "target": "_blank",
            "href2": "https://chatgpt.com",
            "target2": "_blank",
        }
        expected_result = expected_result + ' href2="https://chatgpt.com" target2="_blank"'
        node2 = HTMLNode(tag="b", value="link", children=None, props=prop_case2)
        self.assertEqual(str(node2.props_to_html()), expected_result)

    def test_properNode(self):
        
        prop_case = {
            "href": "https://www.google.com",
            "target": "_blank",
            }
        node = HTMLNode(tag="h1", value="HEADER", children=None, props=prop_case)
        expected_result = "HTMLNode(tag:h1, value:HEADER, children:[], props:{'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(repr(str(node)), repr(expected_result))

    def test_HTMLNodeChild(self):
        node = LeafNode("p", "This is a paragraph of text.").to_html()
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node, expected)

    def test_leaf_to_html_a(self):
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        expected2 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(repr(node2), repr(expected2))

    def test_leaf_to_html_flat_paragraph(self):
        node3 = LeafNode("p", "This is a paragraph of text.").to_html()
        expected3 = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node3, expected3)
    
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    
    def test_leaf_no_value_err(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

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

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestExctractingTitle(unittest.TestCase):
    def test_extract_title(self):
        data = "# Hello, world! "
        expected_result = "Hello, world!"
        self.assertEqual(extract_title(data), expected_result)

    def test_extract_title_bigger_block(self):
        data = "# Hello, world! \n ## This is a subheading"
        expected_result = "Hello, world!"
        self.assertEqual(extract_title(data), expected_result)
    
    def test_extract_title_multiline_block(self):
        data = """
# This is the title
## This is a subheading
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        expected_result = "This is the title"
        self.assertEqual(extract_title(data), expected_result)