from enum import Enum

from htmlnode import HTMLNode
from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    normalized_blocks = []

    # Loop over the split blocks
    for block in split_blocks:
        # skip empty blocks
        if not block.strip():
            continue

        # Split blocks into lines, strip each line, then rejoin
        lines = block.strip().split("\n")
        normalized_lines = [line.strip() for line in lines]
        rejoined_block = "\n".join(normalized_lines)
        normalized_blocks.append(rejoined_block)

    return normalized_blocks


def block_to_block_type(block):
    """
    Headings start with 1-6 # characters, followed by a space and then the heading text.
    Code blocks must start with 3 backticks and end with 3 backticks.
    Every line in a quote block must start with a > character.
    Every line in an unordered list block must start with a - character, followed by a space.
    Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    If none of the above conditions are met, the block is a normal paragraph.
    """
    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        heading_level = 0
        for char in block:
            if char == "#":
                heading_level += 1
            elif char == " ":
                break
            else:
                return (
                    BlockType.PARAGRAPH
                )  # If the function encounters a non-# character before a space, it's not a valid heading
        if 1 <= heading_level <= 6 and block[heading_level] == " ":
            return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in block.split("\n")):
        lines = block.split("\n")
        expected_prefix = "- "

        for line in lines:
            if not line.startswith(expected_prefix):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        lines = block.split("\n")
        expected_number = 1

        for line in lines:
            # check if line starts with the expected number
            expected_prefix = f"{expected_number}. "
            if not line.startswith(expected_prefix):
                return BlockType.PARAGRAPH
            expected_number += 1

        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    # create parent node
    parent_node = HTMLNode(tag="div", children=[])

    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # Process each block
    for block in blocks:
        # Determining block type
        block_type = block_to_block_type(block)

        # Create the appropriate HTMLNode for the block
        html_node = create_html_node(block_type, block)

        # Append to the parent node
        if parent_node.children is None:
            parent_node.children = [html_node]
        else:
            parent_node.children.append(html_node)

    return parent_node


def text_to_children(text):
    text = text.replace("\n", " ")
    text_node = TextNode(text, TextType.TEXT)
    # Using spliting delimeters  to handle delimiters
    text_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)

    # Splitting image and links
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_image(text_nodes)
    # Convert TextNode to HTMLNode
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)

    return html_nodes


def create_html_node(block_type, content):
    # Creates a new HTMLNode with proper data
    if block_type == BlockType.PARAGRAPH:
        children = text_to_children(content)
        return HTMLNode("p", None, children)

    # For headings I have to determine the level of the heading
    elif block_type == BlockType.HEADING:
        level = 0
        for char in content:
            if char == "#":
                level += 1
            else:
                break

        clean_content = content[level:].strip()
        children = text_to_children(clean_content)
        return HTMLNode(f"h{level}", None, children)

    # For code it is a another case, it should not do any inline markdown parsing of its children
    # Manually make a TextNode and use text_node_to_html_node
    elif (
        block_type == BlockType.CODE
    ):  # Strip the triple backticks from the block content
        code_content = content.strip("```").strip()

        # Ensure content ends with newline
        code_content += "\n"
        # Create a node with <pre> as the parent and <code> inside it
        pre_node = HTMLNode(
            tag="pre", children=[HTMLNode(tag="code", value=code_content)]
        )
        return pre_node

    elif block_type == BlockType.QUOTE:
        children = text_to_children(content)
        return HTMLNode("blockquote", None, children)

    elif block_type == BlockType.UNORDERED_LIST:
        # Split content into lines
        items = content.splitlines()
        children = [
            HTMLNode("li", None, text_to_children(item.strip("- ")))
            for item in items
            if item.strip()
        ]
        return HTMLNode("ul", None, children)
    elif block_type == BlockType.ORDERED_LIST:
        # Doing the same as unordered list
        items = content.splitlines()
        children = [
            HTMLNode("li", None, text_to_children(item.strip("1234567890. ")))
            for item in items
            if item.strip()
        ]
        return HTMLNode("ol", None, children)
