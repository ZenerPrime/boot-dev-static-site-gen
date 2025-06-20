import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_p_with_props(self):
		node = LeafNode("p", "Hello, world!", props={ "attrib":"Value" })
		self.assertEqual(node.to_html(), '<p attrib="Value">Hello, world!</p>')

	def test_leaf_to_html_no_tag(self):
		node = LeafNode(None, "Hello, world!", props={ "attrib":"Value" })
		self.assertEqual(node.to_html(), "Hello, world!")

if __name__ == "__main__":
    unittest.main()
