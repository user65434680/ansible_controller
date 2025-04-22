#!/usr/bin/env python3

import shutil
import os
from projects.project_context import get_current_project_number

current_project_number = get_current_project_number()

copy_map = {
    "allowed_domains.json": f"projects/{current_project_number}/allowed_domains.json",
    "placeholder2.json": f"projects/{current_project_number}/placeholder2.json",
    "placeholder3.json": f"projects/{current_project_number}/placeholder3.json",
}

paste_map = {
    "allowed_domains.json": "unbound_default",
    "placeholder2.json": "project/1",
    "placeholder3.json": "project/1",
}

def copy_file(filename):
    """Copy a file from its source in copy_map to its destination in paste_map."""
    source_path = copy_map.get(filename)
    destination_dir = paste_map.get(filename)

    if source_path and destination_dir:
        os.makedirs(destination_dir, exist_ok=True)
        dest_path = os.path.join(destination_dir, filename)
        shutil.copy(source_path, dest_path)
        print(f"Copied {filename} from {source_path} to {dest_path}")
    else:
        print(f"Missing source or destination for {filename}")

def delete_file(filename):
    """Delete a file from its destination in paste_map."""
    destination_dir = paste_map.get(filename)

    if destination_dir:
        dest_path = os.path.join(destination_dir, filename)
        if os.path.exists(dest_path):
            os.remove(dest_path)
            print(f"Deleted {dest_path}")
        else:
            print(f"File not found to delete: {dest_path}")
    else:
        print(f"Destination not found for {filename}")