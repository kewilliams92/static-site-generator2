from os import listdir, mkdir, path
from shutil import copy, rmtree

from copystatic import copy_files_recursive
from htmlnode import LeafNode
from textnode import TextNode, TextType

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    # textnode = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
    # print(textnode)
    # htmlnode = LeafNode("p", "This is a paragraph")
    # htmlnode2 = LeafNode("a", "This is a link", {"href": "https://boot.dev"})
    # print(htmlnode)
    # print(htmlnode2)
    if path.exists(dir_path_public):
        print(f"Removing {dir_path_public}...")
        rmtree(dir_path_public)

    print(f"Copying {dir_path_static} to {dir_path_public}...")
    copy_files_recursive(dir_path_static, dir_path_public)
    print("Done!")


main()
