import unittest

from main import text_node_to_html_node, text_to_textnodes, markdown_to_blocks, markdown_to_html_node, print_nodes
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

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        parsed_nodes = text_to_textnodes(text)
        expectedNodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]        
        self.assertListEqual(parsed_nodes, expectedNodes)


    def test_text_to_textnodes_trailing_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and **some** more text"
        parsed_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("some", TextType.BOLD),
            TextNode(" more text", TextType.TEXT),
        ]        
        self.assertListEqual(parsed_nodes, expected_nodes)

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

    def test_markdown_to_blocks_excessive_newlines(self):
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
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_orderedlist(self):
        md = """
1. One!! HA! HA! HA!
2. TWO!!!!! HA! HA! HA!
3. THREE!!!!!  HA! HA! HA!
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>One!! HA! HA! HA!</li><li>TWO!!!!! HA! HA! HA!</li><li>THREE!!!!!  HA! HA! HA!</li></ol></div>",
        )

    def test_unorderedlist(self):
        md = """
- One!! HA! HA! HA!
- TWO!!!!! HA! HA! HA!
- THREE!!!!!  HA! HA! HA!
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>One!! HA! HA! HA!</li><li>TWO!!!!! HA! HA! HA!</li><li>THREE!!!!!  HA! HA! HA!</li></ul></div>",
        )

    def test_quote(self):
        md = """
> One!! HA! HA! HA!
> TWO!!!!! HA! HA! HA!
> THREE!!!!!  HA! HA! HA!
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>One!! HA! HA! HA!\nTWO!!!!! HA! HA! HA!\nTHREE!!!!!  HA! HA! HA!</blockquote></div>",
        )



    def test_heading_quote(self):
        md = """
### Heading!

> One!! HA! HA! HA!
> TWO!!!!! HA! HA! HA!
> THREE!!!!!  HA! HA! HA!
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Heading!</h3><blockquote>One!! HA! HA! HA!\nTWO!!!!! HA! HA! HA!\nTHREE!!!!!  HA! HA! HA!</blockquote></div>",
        )