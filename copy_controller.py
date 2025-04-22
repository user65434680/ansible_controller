#!/usr/bin/env python3

import shutil
import os
from projects.project_context import get_current_project_number

current_project_number = get_current_project_number()

copy_map = {
    "allowed_domains.json": f"projects/{current_project_number}/allowed_domains.json",
    "whitelist.json": f"projects/{current_project_number}/whitelist.json",
    "user_data.json": f"projects/{current_project_number}/user_data.json",
    "ranked_clients.json": f"projects/{current_project_number}/ranked_clients.json",
}

paste_map = {
    "allowed_domains.json": "unbound_default",
    "whitelist.json": "apparmor_default",
    "user_data.json": "users_default",
    "ranked_clients.json": "clients_default",
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