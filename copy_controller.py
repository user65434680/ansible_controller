#!/usr/bin/env python3

import importlib.util
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

def copy_file(source, destination):
    shutil.copy(source, destination)

def delete_file(path):
    os.remove(path)

def run_copy_process(filename):
    source_path = copy_map.get(filename)
    destination_dir = paste_map.get(filename)
    
    if source_path and destination_dir:
        dest_path = os.path.join(destination_dir, filename)
        copy_file(source_path, dest_path)
        print(f"Copied {filename} to {destination_dir}")
        return dest_path
    else:
        print(f"Missing source or destination for {filename}")
        return None

def delete_needed_file(filename):
    destination_dir = paste_map.get(filename)
    
    if destination_dir:
        dest_path = os.path.join(destination_dir, filename)
        if os.path.exists(dest_path):
            delete_file(dest_path)
            print(f"Deleted {dest_path}")
        else:
            print(f"File not found to delete: {dest_path}")
    else:
        print(f"Destination not found for {filename}")