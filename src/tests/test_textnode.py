import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_not_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a not text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_not_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_not_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "http:\\somewhere.url")
        self.assertNotEqual(node, node2)

    def test_repr_not_equal(self):
        node = repr(TextNode("This is a text node", TextType.BOLD, None))
        node2 = repr(TextNode("This is a text node", TextType.BOLD, "http:\\somewhere.url"))

        self.assertNotEqual(node, node2)

    def test_repr_equal(self):
        node = repr(TextNode("This is a text node", TextType.BOLD))
        node2 = repr(TextNode("This is a text node", TextType.BOLD, None))

        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
