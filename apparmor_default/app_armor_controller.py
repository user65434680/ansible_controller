#!/usr/bin/env python3

import os 
import json
from ansible_utils import run_ansible_playbook
from projects.project_context import get_current_project_number
from copy_controller import copy_file, delete_file

current_project_number = get_current_project_number()

c_path = os.path.dirname(os.path.abspath(__file__))

def generate_profile(path):
    return f"""#include <tunables/global>

{path} {{
  {path} rix,
}}
"""

projects_path = os.path.join(os.path.dirname(c_path), "projects")
WHITELIST_FILE = os.path.join(projects_path, current_project_number, "whitelist.json")

# Segment 1: Whitelist Management
def load_whitelist():
    """Load the whitelist.json if it exists."""
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, "r") as f:
            return json.load(f)
    return {"whitelist": []}

def save_whitelist(data):
    """Save the updated whitelist to the JSON file."""
    with open(WHITELIST_FILE, "w") as f:
        json.dump(data, f, indent=2)

def main_1():
    """Main function to add applications to the whitelist."""
    whitelist = load_whitelist()

    while True:
        path = input("Enter the full path to the application (or 'done' to finish): ").strip()
        if path.lower() == "done":
            break
        if not os.path.exists(path):
            print("That path doesn't exist. Please try again.")
            continue
        name = os.path.basename(path)
        profile = generate_profile(path)
        whitelist["whitelist"].append({
            "app_name": name,
            "path": path,
            "profile": profile
        })
        print(f"Added {path} to whitelist.")

    save_whitelist(whitelist)
    print(f"\nSaved to {WHITELIST_FILE}")

def control_whitelist():
    """Control options for managing the whitelist."""
    data1 = input("Choose\n1) Add to whitelist\n2) Remove from whitelist\n3) Exit\n").strip()

    if data1 == "1":
        main_1()
    elif data1 == "2":
        run_ansible_playbook(f"{c_path}/remove_whitelist.yml")
        print("Whitelist cleared")
    elif data1 == "3":
        return
    else:
        print("Invalid choice. Please try again.")
        control_whitelist()

# Segment 2: Blacklist Management
def control_blacklist():
    """Control options for managing the blacklist."""
    data2 = input("Choose\n1) Create blacklist and deny all apps\n2) Remove blacklist and disable all apps\n3) Exit\n").strip()

    if data2 == "1":
        print("Placeholder for creating blacklist")
    elif data2 == "2":
        print("Placeholder for removing blacklist")
    elif data2 == "3":
        return
    else:
        print("Invalid choice. Please try again.")
        control_blacklist()

def app_armor_menu():
    """Main menu for AppArmor configuration."""
    print("AppArmor Menu")
    print("1. Control whitelist")
    print("2. Control blacklist")
    print("3. Push to client")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        control_whitelist()
    elif choice == '2':
        control_blacklist()
    elif choice == '3':
        copy_file("whitelist.json")
        run_ansible_playbook(f"{c_path}/whitelist_apps.yml")
        delete_file("whitelist.json")
    elif choice == '4':
        return
    else:
        print("Invalid choice. Please try again.")
        app_armor_menu()

if __name__ == "__main__":
    app_armor_menu()
