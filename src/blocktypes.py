import re

from enum import Enum

class BlockTypes(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"
	
def block_to_block_type(block):
	if is_heading_block(block):
		return BlockTypes.HEADING
	elif is_code_block(block):
		return BlockTypes.CODE
	elif is_quote_block(block):
		return BlockTypes.QUOTE
	elif is_unordered_list_block(block):
		return BlockTypes.UNORDERED_LIST
	elif is_ordered_list_block(block):
		return BlockTypes.ORDERED_LIST
    
	return BlockTypes.PARAGRAPH

def is_heading_block(block):
	return re.fullmatch(r"#{1,6} {1}.*", block) is not None

def is_code_block(block):
	return re.fullmatch(r"`{3}(?:.*\n*)*`{3}", block) is not None

def is_quote_block(block):
	return re.fullmatch(r"(?:>\s.*\n?)+", block) is not None

def is_unordered_list_block(block):
	return re.fullmatch(r"(?:- .+\n?)+", block) is not None

def is_ordered_list_block(block):
	if re.fullmatch(r"(?:\d+. .+\n?)+", block) is None:
		return False
	return is_ordered_list_in_sequence(list(map(lambda l: l.split(". ", 1)[0], block.split("\n"))))

def is_ordered_list_in_sequence(numbers):
    if not numbers:
        return False  # Empty list is not considered incremented
    for i in range(len(numbers) - 1):
        l = numbers[i+1]
        r = numbers[i]
        if not l.isnumeric() or not r.isnumeric() or int(l) - int(r) != 1:
            return False
    return True