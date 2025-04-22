#!/usr/bin/env python3

import importlib.util
import shutil
import os
from projects.project_context import get_current_project_number

current_project_number = get_current_project_number()

copy_map = {
    "placeholder.json": f"projects/{current_project_number}/placeholder.json",
    "placeholder2.json": f"projects/{current_project_number}/placeholder.json",
    "placeholder3.json": f"projects/{current_project_number}/placeholder.json"
}

paste_map = {
    "placeholder.json": "project/1",
    "placeholder2.json": "project/1",
    "placeholder3.json": "project/1"
}

def get_needed_file(script_path):
    spec = importlib.util.spec_from_file_location("temp_module", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "NEEDED_FILE", None)

def copy_file(source, destination):
    shutil.copy(source, destination)

def delete_file(path):
    os.remove(path)

def run_copy_process(script_path):
    needed_file = get_needed_file(script_path)
    if needed_file:
        source_path = copy_map.get(needed_file)
        destination_dir = paste_map.get(needed_file)
        if source_path and destination_dir:
            dest_path = os.path.join(destination_dir, needed_file)
            copy_file(source_path, dest_path)
            os.system(f"python3 {script_path}")
            delete_file(dest_path)
        else:
            print("Missing source or destination for", needed_file)
    else:
        print("Script didn't define NEEDED_FILE")

def delete_needed_file(script_path):
    needed_file = get_needed_file(script_path)
    if needed_file:
        destination_dir = paste_map.get(needed_file)
        if destination_dir:
            dest_path = os.path.join(destination_dir, needed_file)
            if os.path.exists(dest_path):
                delete_file(dest_path)
            else:
                print("File not found to delete:", dest_path)
        else:
            print("Destination not found for", needed_file)
    else:
        print("Script didn't define NEEDED_FILE")

if __name__ == "__main__":
    script_path = "project/1/placeholder.py"
    run_copy_process(script_path)
