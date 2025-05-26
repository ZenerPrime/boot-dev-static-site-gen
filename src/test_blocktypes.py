import unittest

from blocktypes import BlockTypes, block_to_block_type


class TestBlockTypes(unittest.TestCase):

    def test_block_to_block_type_heading(self):
        block = "##### This is a heading"
        parsed_block_type = block_to_block_type(block)
        self.assertEqual(BlockTypes.HEADING, parsed_block_type)

    def test_block_to_block_type_code(self):
        block = "```This is a heading```"
        parsed_block_type = block_to_block_type(block)
        self.assertEqual(BlockTypes.CODE, parsed_block_type)

    def test_block_to_block_type_code_multiline(self):
        block = "```\nThis is a heading\na bit more code```"
        parsed_block_type = block_to_block_type(block)
        self.assertEqual(BlockTypes.CODE, parsed_block_type)

    def test_block_to_block_type_quote(self):
        block = "> this is a quote"
        parsed_block_type = block_to_block_type(block)
        self.assertEqual(BlockTypes.QUOTE, parsed_block_type)

    def test_block_to_block_type_quote_multiline(self):
        block = "> this is a quote\n> continued quote"
        parsed_block_type = block_to_block_type(block)
        self.assertEqual(BlockTypes.QUOTE, parsed_block_type)

    def test_block_to_block_type_unordered_list(self):
        block = "- this is a quote"
        parsed_block_type = block_to_block_type(block)
        self.assertEqual(BlockTypes.UNORDERED_LIST, parsed_block_type)

    def test_block_to_block_type_unordered_list_multiline(self):
        block = "- this is a quote\n- continued quote"
        parsed_block_type = block_to_block_type(block)
        self.assertEqual(BlockTypes.UNORDERED_LIST, parsed_block_type)

    def test_block_to_block_type_ordered_list(self):
        block = "1. this is a quote"
        parsed_block_type = block_to_block_type(block)
        self.assertEqual(BlockTypes.ORDERED_LIST, parsed_block_type)

    def test_block_to_block_type_ordered_list_multiline(self):
        block = "1. this is a quote\n2. continued quote"
        parsed_block_type = block_to_block_type(block)
        self.assertEqual(BlockTypes.ORDERED_LIST, parsed_block_type)

    def test_block_to_block_type_ordered_list_out_of_sequence(self):
        block = "2. this is a quote\n1. continued quote"
        parsed_block_type = block_to_block_type(block)
        self.assertEqual(BlockTypes.PARAGRAPH, parsed_block_type)

    def test_block_to_block_type_ordered_list_multiline_invalid(self):
        block = "1. this is a quote\na. continued quote"
        parsed_block_type = block_to_block_type(block)
        self.assertEqual(BlockTypes.PARAGRAPH, parsed_block_type)