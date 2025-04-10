from os import listdir, mkdir, path
from shutil import copy, rmtree

from htmlnode import LeafNode
from textnode import TextNode, TextType


def main():
    textnode = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
    print(textnode)
    htmlnode = LeafNode("p", "This is a paragraph")
    htmlnode2 = LeafNode("a", "This is a link", {"href": "https://boot.dev"})
    print(htmlnode)
    print(htmlnode2)


main()
