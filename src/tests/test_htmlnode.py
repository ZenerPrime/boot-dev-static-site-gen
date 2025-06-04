import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HTMLNode(tag = "div", value = "Some Text", props = {
            "href": "https://www.google.com",
            "target": "_blank",
        })

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_without_props(self):
        node = HTMLNode(tag = "div", value = "Some Text")

        self.assertEqual(node.props_to_html(), '')

    def test_to_html_is_not_imlemented(self):
        node = HTMLNode(tag = "div", value = "Some Text")

        with self.assertRaises(NotImplementedError):
            node.to_html()

        
if __name__ == "__main__":
    unittest.main()