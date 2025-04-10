import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception("Invalid markdown")
        for i, section in enumerate(sections):
            if section:
                if i % 2 == 0:
                    split_nodes.append(TextNode(section, TextType.TEXT))
                else:
                    split_nodes.append(TextNode(section, text_type))
        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # Skip non-text nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # Extract images from current node
        images = extract_markdown_images(old_node.text)

        # If no images are found keep the original node
        if not images:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        # Now handle the text splitting
        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"
            parts = remaining_text.split(image_markdown, 1)  # split only once

            # Add text before image if not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # Update remaining text
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # Skip non-text nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # Extract links from current node
        links = extract_markdown_links(old_node.text)

        # If no links are found keep the original node
        if not links:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        # Now handle the text splitting
        for text, url in links:
            link_markdown = f"[{text}]({url})"
            parts = remaining_text.split(link_markdown, 1)  # split only once

            # Add text before link if not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the link node
            new_nodes.append(TextNode(text, TextType.LINK, url))

            # Update remaining text
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


# Final function
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
