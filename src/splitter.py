import re

from textnode import TextNode, TextType

def extract_markdown_images(text):
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	
def extract_markdown_links(text):
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)		

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for node in old_nodes.copy():
		new_nodes.extend(split_single_node_delimiter(node, delimiter, text_type))
	return new_nodes

def split_single_node_delimiter(node, delimiter, text_type):
	new_nodes = []
	if node.text_type != TextType.TEXT:
		new_nodes.append(node)
	else:
		parts = node.text.split(delimiter)
		parts_len = len(parts)
		if (parts_len > 0):
			for i in range(parts_len):
				if i % 2 == 0:
					new_nodes.append(TextNode(parts[i], node.text_type))
				else:
					new_nodes.append(TextNode(parts[i], text_type))
		else:
			new_nodes.append(node)
	return new_nodes

def split_nodes_image(old_nodes):
	new_nodes = []
	for node in old_nodes.copy():
		new_nodes.extend(spit_single_node_image(node))
	return new_nodes

def spit_single_node_image(node):
	new_nodes = []
	if node.text_type != TextType.TEXT:
		return [node]
	else:
		text = node.text
		matches = extract_markdown_images(text)
		for match in matches:
			image_part = f"![{match[0]}]({match[1]})"
			section = text.split(image_part, 1)
			new_nodes.extend([TextNode(section[0], TextType.TEXT),TextNode(match[0], TextType.IMAGE, match[1])])
			text = "" if len(section) <= 1 else section[1]
		if len(text) > 0:
			new_nodes.append(TextNode(text, TextType.TEXT))
			
	return new_nodes

def split_nodes_link(old_nodes):
	new_nodes = []
	for node in old_nodes.copy():
		new_nodes.extend(spit_single_node_link(node))
	return new_nodes

def spit_single_node_link(node):
	new_nodes = []
	if node.text_type != TextType.TEXT:
		return [node]
	else:
		text = node.text
		matches = extract_markdown_links(text)
		i = 0
		for match in matches:
			i += 1
			image_part = f"[{match[0]}]({match[1]})"
			section = text.split(image_part, 1)
			new_nodes.extend([TextNode(section[0], TextType.TEXT),TextNode(match[0], TextType.LINK, match[1])])
			text = "" if len(section) <= 1 else section[1]
		if len(text) > 0:
			new_nodes.append(TextNode(text, TextType.TEXT))

	return new_nodes
