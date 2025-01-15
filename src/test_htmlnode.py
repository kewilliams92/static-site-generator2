import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HtmlNode(props={"href": "https://boot.dev", "target": "_blank"})
        expected_output = ' href="https://boot.dev" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_empty_props(self):
        node = HtmlNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        node = HtmlNode(props=None)
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_props_to_html_no_tag(self):
        node = LeafNode(None, "This is a paragraph")
        self.assertEqual(node.to_html(), "This is a paragraph")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_output = (
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        self.assertEqual(node.to_html(), expected_output)

    # testing nested parent nodes
    def test_to_html_nested_parent_nodes(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "a",
                    [
                        LeafNode("span", "favorite social media"),
                    ],
                    {"href": "https://www.facebook.com"},
                ),
            ],
        )
        expected_output = '<div><b>Bold text</b><a href="https://www.facebook.com"><span>favorite social media</span></a></div>'
        self.assertEqual(node.to_html(), expected_output)

    # testing multiple levels of nesting:
    def test_to_html_nested_parent_nodes_multiple_levels(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "a",
                    [
                        LeafNode("span", "favorite social media"),
                        ParentNode(
                            "div",
                            [
                                LeafNode("p", "This is a paragraph"),
                            ],
                        ),
                    ],
                    {"href": "https://www.facebook.com"},
                ),
            ],
        )
        expected_output = '<div><b>Bold text</b><a href="https://www.facebook.com"><span>favorite social media</span><div><p>This is a paragraph</p></div></a></div>'
        self.assertEqual(node.to_html(), expected_output)

    # test invalid html: no tag
    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "Bold text")])
        with self.assertRaises(ValueError):
            node.to_html()

    # test invalid children: no children
    def test_to_html_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    # test multiple siblings
    def test_to_html_multiple_siblings(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                LeafNode("i", "italic text"),
                LeafNode("u", "underline text"),
            ],
        )
        expected_output = (
            "<div><b>Bold text</b><i>italic text</i><u>underline text</u></div>"
        )
        self.assertEqual(node.to_html(), expected_output)


if __name__ == "__main__":
    unittest.main()
