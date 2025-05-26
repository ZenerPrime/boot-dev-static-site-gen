
from textnode import TextNode, TextType
from leafnode import LeafNode
from splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link

def text_node_to_html_node(text_node):
	if (not isinstance(text_node, TextNode)):
		raise ValueError("text_node must be a TextNode")
	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(tag=None, value=text_node.text)
		case TextType.BOLD:
			return LeafNode(tag="b", value=text_node.text)
		case TextType.ITALIC:
			return LeafNode(tag="i", value=text_node.text)
		case TextType.CODE:
			return LeafNode(tag="code", value=text_node.text)
		case TextType.LINK:
			return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
		case TextType.IMAGE:
			return LeafNode(tag="img", value="", props={"src":text_node.url, "alt":text_node.text})
		

def text_to_textnodes(text):
	return split_nodes_link(
		split_nodes_image(
			split_nodes_delimiter(
				split_nodes_delimiter(
					split_nodes_delimiter(
						[TextNode(text, TextType.TEXT)]
						, "**", TextType.BOLD)
					, "_", TextType.ITALIC)
				, "`", TextType.CODE)
			)
		)

def print_nodes(text, nodes):
	print(text)
	for i in range(len(nodes)):
		print(f"Node {i}\n\t{nodes[i]}")

def main():
	pass

main()