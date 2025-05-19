import unittest

from main import text_node_to_html_node
from textnode import TextNode, TextType

class TestMain(unittest.TestCase):
    def test_text(self):
        text = "This is a text node"
        expected_tag = None
        text_type = TextType.TEXT
        node = TextNode(text, text_type)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, text)
        self.assertEqual(html_node.to_html(), text)
    
    def test_bold(self):
        text = "This is a bold node"
        expected_tag = "b"
        text_type = TextType.BOLD
        node = TextNode(text, text_type)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, text)
        self.assertEqual(html_node.to_html(), f"<{expected_tag}>{text}</{expected_tag}>")

    def test_italic(self):
        text = "This is a italic node"
        expected_tag = "i"
        text_type = TextType.ITALIC
        node = TextNode(text, text_type)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, text)
        self.assertEqual(html_node.to_html(), f"<{expected_tag}>{text}</{expected_tag}>")

    def test_code(self):
        text = "This is a code node"
        expected_tag = "code"
        text_type = TextType.CODE
        node = TextNode(text, text_type)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, text)
        self.assertEqual(html_node.to_html(), f"<{expected_tag}>{text}</{expected_tag}>")

    def test_link(self):
        text = "This is a link node"
        expected_url = "http://www.google.com"
        expected_tag = "a"        
        text_type = TextType.LINK
        node = TextNode(text, text_type, expected_url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, text)
        self.assertEqual(html_node.to_html(), f'<{expected_tag} href="{expected_url}">{text}</{expected_tag}>')

    def test_image(self):
        text = "This is an image node"
        expected_url = "http://www.google.com/img.png"
        expected_tag = "img"        
        text_type = TextType.IMAGE
        node = TextNode(text, text_type, expected_url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, {"src":expected_url, "alt":text})
        self.assertEqual(html_node.to_html(), f'<{expected_tag} src="{expected_url}" alt="{text}"></img>')        
