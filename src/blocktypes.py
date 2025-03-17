from enum import Enum
import re
from nodedelimiter import text_to_textnodes, text_node_to_html_node
from htmlnode import *
from textnode import *

class BlockType(Enum):  ##declare enum types
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(text): #take text from markdown file
    blocks = text.split("\n\n") ##split the text into blocks
    filtered_blocks = [] 
    for block in blocks: 
        if block == "": #if block is empty
            continue   #skip the block
        block = block.strip()   #we remove any whitespaces from the block at the start and end
        filtered_blocks.append(block) #append block
    return filtered_blocks #return the filtered blocks as a list

def block_to_block_type(block): #this determines which blocktype a block is after being cut by markdown_to_blocks, takes blocks and returns enum type
    lines = block.split("\n") #split the block into lines
    #everything below operates on those split lines, iterating over them for multiple line markdown
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")): #check if it starts with hashtags up to 6 to determine which h1 to h6 is it
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"): # check for code
        return BlockType.CODE
    if block.startswith(">"): # check for quote
        for line in lines: # if its quote then we check the following lines
            if not line.startswith(">"): #if any of the lines does not start with > then its normal paragraph
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "): #same as above, check first and if it is unordered list then check all following lines until we find paragraph
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "): # same as above
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH # if none of the above then its a paragraph

def block_to_html_node(block): # this takes a block of markdown text, checks the block type and returns the corresponding html node
    block_type = block_to_block_type(block) # initially block is just a string, this function determines the block type by outermost delimiters
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def markdown_to_html_node(markdown): #helper function, takes raw markdown and returns a parent node (outermost div) containing all the html children nodes
    blocks = markdown_to_blocks(markdown) #split entire markdown text into blocks of markdown
    children = []
    for block in blocks: #change every block into html node with helper functions according to their type
        html_node = block_to_html_node(block)
        children.append(html_node) # append and return parent object with appended children
    return ParentNode("div", children, None) # it is the outermost div

def text_to_children(text): #helper function, changes text into textnodes and then into html nodes
    text_nodes = text_to_textnodes(text) #this takes text and returns list of text nodes with their respective types
    children = []
    for text_node in text_nodes: # iterate over the list of text nodes
        html_node = text_node_to_html_node(text_node) # and change them one by one into html nodes, this is lowest level which returns leaf nodes
        children.append(html_node)
    return children


def paragraph_to_html_node(block): #takes block of markdown text
    lines = block.split("\n") # break into list of lines
    paragraph = " ".join(lines) # join it with spaces, eliminates any line breaks
    children = text_to_children(paragraph) # get children in html node form
    return ParentNode("p", children)


def heading_to_html_node(block): #take block
    level = 0
    for char in block:
        if char == "#":
            level += 1 #count the number of # to determine the heading level
        else:
            break
    if level + 1 >= len(block): #if its only heading without text then block is invalid
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :] # separate heading characters from the text
    children = text_to_children(text) # transform separated text into html nodes
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.NORMAL)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line[2:]
            title = title.strip()
            return title
    raise Exception("no title found")