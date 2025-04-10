import os
import shutil


# This will copy contents from a source directory to a destination directory
def copy_static_recursively(source_dir, destination_dir):
    # if the path doesn't exist, then we should create it
    if not os.path.exists(destination_dir):
        print(f"Creating directory {destination_dir}...")
        os.makedirs(destination_dir)

    # We then iterate through the source directory and copy each file to destination
    for filename in os.listdir(source_dir):
        print(f"Processing {filename}...")
        from_path = os.path.join(source_dir, filename)
        to_path = os.path.join(destination_dir, filename)
        print(f"Copying {from_path} to {to_path}..")
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_static_recursively(from_path, to_path)
