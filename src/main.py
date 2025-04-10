import os
import pathlib
import sys

from copystatic import copy_static_recursively
from generate_page import generate_page_recursively


def main():
    # Check if a base path was provided as a command-line argument
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    print(f"Using basepath: {basepath}")

    # Define paths
    content_dir = "content"
    template_path = "template.html"
    static_dir = "static"
    docs_dir = "docs"

    # Create docs directory if it doesn't exist
    os.makedirs(docs_dir, exist_ok=True)

    # Generate HTML pages from markdown files
    if os.path.exists(content_dir):
        generate_page_recursively(content_dir, template_path, docs_dir, basepath)
    else:
        print(f"Error: Content directory '{content_dir}' not found")

    # Copy static files
    if os.path.exists(static_dir):
        copy_static_recursively(static_dir, docs_dir)
    else:
        print(f"Warning: Static directory '{static_dir}' not found")

    print("Site generation complete!")


if __name__ == "__main__":
    main()
