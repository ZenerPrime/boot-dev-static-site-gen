import os
import shutil

from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from blocktypes import BlockTypes, block_to_block_type

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

def markdown_to_blocks(markdown):
	return list(filter(lambda b: len(b) > 0, map(lambda b: b.strip(), markdown.split("\n\n"))))

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	block_nodes = []
	for block in blocks:
		block_type = block_to_block_type(block)
		block_nodes.append(block_to_html_node(block_type, block))

	return ParentNode(tag="div", children= block_nodes)

def block_to_html_node(block_type, block):
	match block_type:
		case BlockTypes.CODE:
			children = [text_node_to_html_node(TextNode(block.strip("`"), TextType.CODE))]
			return ParentNode("pre", children=children)
		case BlockTypes.HEADING:
			parts = block.split(" ", 1)
			text = parts[1]			
			return ParentNode(f"h{len(parts[0])}", children=text_to_children(text))
		case BlockTypes.QUOTE:
			text = "\n".join(map(lambda l: l.lstrip("> "), block.split("\n")))
			return ParentNode("blockquote", children=text_to_children(text))
		case BlockTypes.PARAGRAPH:
			return ParentNode("p", children=text_to_children(" ".join(block.split("\n"))))
		case BlockTypes.UNORDERED_LIST:
			lines = map(lambda l: l.lstrip("- "), block.split("\n"))
			line_items = []
			for line in lines:
				line_items.append(ParentNode("li", children=text_to_children(line)))
			return ParentNode("ul", children=line_items)
		case BlockTypes.ORDERED_LIST:
			lines = map(lambda l: l.split(" ", 1)[1], block.split("\n"))
			line_items = []
			for line in lines:
				line_items.append(ParentNode("li", children=text_to_children(line)))
			return ParentNode("ol", children=line_items)		

def text_to_children(text):
	children = []
	for text_node in text_to_textnodes(text):
		children.append(text_node_to_html_node(text_node))
	return children
	
def print_nodes(text, nodes):
	print(text)
	for i in range(len(nodes)):
		print(f"Node {i}\n\t{nodes[i]}")

def copy_tree(source_dir, destination_dir):	
	print(f"checking {destination_dir}")
	if os.path.exists(destination_dir):
		print(f"{destination_dir} exists. so deleting it")
		shutil.rmtree(destination_dir, ignore_errors=True)
	
	print(f"checking {source_dir}")
	if not os.path.exists(source_dir):			
		print(f"{source_dir} doesn't exists. so returning")
		return
	
	print(f"making {destination_dir}")
	os.mkdir(destination_dir)

	print(f"enumerating {source_dir}")
	for entry in os.listdir(source_dir):
		print(f"found {entry}")
		entry_source = os.path.join(source_dir, entry)
		entry_dest = os.path.join(destination_dir, entry)
		print(f"entry source {entry_source}")
		print(f"entry destination {entry_dest}")
		if (os.path.isfile(entry_source)):
			print(f"{entry} is a file and will be copied")
			shutil.copy(entry_source, entry_dest)
		else:
			print(f"{entry} is a directory and will have th tree copied")
			copy_tree(entry_source, entry_dest)

def generate_pages_recursive(dir_path_content, template_path, dir_path_dest):
	for entry in os.listdir(dir_path_content):
		entry_path = os.path.join(dir_path_content, entry)
		dest_path = os.path.join(dir_path_dest, entry)
		if os.path.isfile(entry_path):
			if entry_path.endswith(".md"):
				dest_path = dest_path.rstrip(".md") + ".html"
				generate_page(entry_path, template_path, dest_path)
		else:
			generate_pages_recursive(entry_path, template_path, dest_path)

def extract_title(markdown):
	title = next(filter(lambda l: l.startswith("# "), markdown.split("\n")), None)
	return None if title == None else title.lstrip("# ")

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	with open(from_path) as from_file:
		markdown = from_file.read()
	with open(template_path) as template_file:
		template = template_file.read()
	title = extract_title(markdown)
	content = markdown_to_html_node(markdown).to_html()
	output = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
	os.makedirs(os.path.dirname(dest_path), exist_ok=True)
	with open(dest_path, mode="w+t") as dest_file:
		dest_file.write(output)



def main():
	copy_tree("static", "public")
	generate_pages_recursive("content", "template.html", "public")

main()