import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_split_node_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        delimiter = "**"
        text_type = TextType.BOLD
        result = split_nodes_delimiter([node], delimiter, text_type)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_node_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        delimiter = "`"
        text_type = TextType.CODE
        result = split_nodes_delimiter([node], delimiter, text_type)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_node_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        delimiter = "*"
        text_type = TextType.ITALIC
        result = split_nodes_delimiter([node], delimiter, text_type)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    # def test_nested_delimiters(self):
    #     node = TextNode("This is **nested *bold***", TextType.TEXT)
    #     delimiter = "**"
    #     text_type = TextType.BOLD
    #     result = split_nodes_delimiter([node], delimiter, text_type)
    #     expected = [
    #         TextNode("This is ", TextType.TEXT),
    #         TextNode("nested *bold*", TextType.BOLD),
    #     ]
    #     self.assertEqual(result, expected)

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_split_node_invalid_markdown(self):
        node = TextNode("This is **bold text", TextType.TEXT)
        delimiter = "**"
        text_type = TextType.BOLD
        # Assert an exception is raised
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], delimiter, text_type)

        self.assertEqual(str(context.exception), "Invalid markdown")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://boot.dev)")
        self.assertListEqual([("link", "https://boot.dev")], matches)


if __name__ == "__main__":
    unittest.main()
