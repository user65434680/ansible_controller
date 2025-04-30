#!/usr/bin/env python3

import os 
import json
from projects.project_context import get_current_project_number
from projects.pending_control import add_to_pending

current_project_number = get_current_project_number()

c_path = os.path.dirname(os.path.abspath(__file__))

def generate_profile(path):
    return f"""profile {path} flags=(attach_disconnected) {{
    # Deny for everyone by default
    deny {path} rix,

    # Allow for users in sudo group (add subprofiles manually as needed)
    # Example for user 'admin' in sudo group:
    profile admin {path} flags=(attach_disconnected) {{
        allow {path} rix,
    }}
}}"""


projects_path = os.path.join(os.path.dirname(c_path), "projects")
blacklist_FILE = os.path.join(projects_path, current_project_number, "blacklist.json")



def load_blacklist():
    """Load blacklist.json if it exists."""
    if os.path.exists(blacklist_FILE):
        with open(blacklist_FILE, "r") as f:
            return json.load(f)
    return {"blacklist": []}

def save_blacklist(data):
    """Save the updated blacklist to the JSON file."""
    with open(blacklist_FILE, "w") as f:
        json.dump(data, f, indent=2)

def main_1():
    """Main function to add applications to the blacklist."""
    blacklist = load_blacklist()

    while True:
        path = input("Enter the full path to the application (or 'done' to finish): ").strip()
        if path.lower() == "done":
            break
        if not os.path.exists(path):
            print("That path doesn't exist. Please try again.")
            continue
        name = os.path.basename(path)
        profile = generate_profile(path)
        blacklist["blacklist"].append({
            "app_name": name,
            "path": path,
            "profile": profile
        })
        print(f"Added {path} to blacklist.")

    save_blacklist(blacklist)
    print(f"\nSaved to {blacklist_FILE}")

def control_blacklist():
    """Control options for managing the blacklist."""
    data1 = input("Choose\n1) Add to blacklist\n2) Remove from blacklist\n3) Exit\n").strip()

    if data1 == "1":
        main_1()
    elif data1 == "2":
        print("Adding clear blacklist to pending changes...")
        add_to_pending(projects_path, current_project_number, "apparmor_changes", "remove_blacklist.yml")
    elif data1 == "3":
        return
    else:
        print("Invalid choice. Please try again.")
        control_blacklist()

def app_armor_menu():
    """Main menu for AppArmor configuration."""
    print("AppArmor Menu")
    print("1. Control blacklist")
    print("2. Remove blacklist and reset")
    print("3. Push to client")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        control_blacklist()
    elif choice == '2':
        control_blacklist()
    elif choice == '3':
        print("Adding to pending changes")
        add_to_pending(projects_path, current_project_number, "apparmor_changes", "remove_blacklist.yml")
    elif choice == '4':
        return
    else:
        print("Invalid choice. Please try again.")
        app_armor_menu()

if __name__ == "__main__":
    app_armor_menu()
