import os
import pathlib

from block_markdown import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}..")
    from_file = open(from_path, "r")
    markdown = from_file.read()
    from_file.close()

    template_path = open(template_path, "r")
    template = template_path.read()
    template_path.close()

    # Using markdown_to_html_node function and .to_html method to convert markdown to html node
    node = markdown_to_html_node(markdown)
    html = node.to_html()

    # Grabbing the title fro mthe page
    title = extract_title(markdown)

    # Using string formatting to fill in the template with the title and content
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    # Replace href and src attributes with the basepath
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    # Now we write the full HTML page to a file at dest_path, creating any necessary directories if needed
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    # Write the HTML content to the destination file
    with open(dest_path, "w") as dest_file:
        dest_file.write(template)


def generate_page_recursively(
    dir_path_content, template_path, dest_dir_path, basepath="/"
):
    print(
        f"Generating pages from {dir_path_content} {template_path} to {dest_dir_path}.."
    )
    # List all files
    files = os.listdir(dir_path_content)
    # using pathlib.Path to join the path to the file
    for file in files:
        file_path = pathlib.Path(dir_path_content) / file
        if os.path.isfile(file_path):
            if file.endswith(".md"):
                dest_path = pathlib.Path(dest_dir_path) / (file[:-3] + ".html")
                generate_page(file_path, template_path, dest_path, basepath)
        elif os.path.isdir(file_path):
            dest_dir = pathlib.Path(dest_dir_path) / file
            generate_page_recursively(file_path, template_path, dest_dir, basepath)
        elif os.path.isdir(file_path):
            dest_dir = pathlib.Path(dest_dir_path) / file
            generate_page_recursively(file_path, template_path, dest_dir)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No h1 detected in markdown")
