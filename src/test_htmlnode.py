import unittest

from htmlnode import HtmlNode


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


if __name__ == "__main__":
    unittest.main()
