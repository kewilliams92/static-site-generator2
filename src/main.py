from os import path
from shutil import rmtree

from copystatic import copy_files_recursive
from generate_page import generate_page_recursively

dir_path_static = "./static"
dir_path_public = "./public"
path_template = "./template.html"
dir_path_content = "./content"


def main():
    if path.exists(dir_path_public):
        print(f"Removing {dir_path_public}...")
        rmtree(dir_path_public)

    print(f"Copying {dir_path_static} to {dir_path_public}...")
    copy_files_recursive(dir_path_static, dir_path_public)

    # Generate pages from all markdown files in content directory
    print(f"Generating pages from {dir_path_content}...")
    generate_page_recursively(dir_path_content, path_template, dir_path_public)
    print("Done!")


main()
