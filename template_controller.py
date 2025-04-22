#!/usr/bin/env python3

import os
import json
import sys
import shutil
from projects.project_context import get_current_project_number

current_project_number = get_current_project_number()
c_path = os.path.dirname(os.path.abspath(__file__))

def list_templates():
    template_dir = "templates"
    
    if not os.path.exists(template_dir):
        print(f"Template '{template_dir}' does not exist. Creating...")
        os.makedirs(template_dir, exist_ok=True)
        print(f"Template '{template_dir}' created.")
        return
 
    folders = [folder for folder in os.listdir(template_dir) if os.path.isdir(os.path.join(template_dir, folder))]

    if folders:
        print("Available templates: ")
        for folder in folders:
            print(f"- {folder}")
    else:
        print("No templates found.")

def save_template():
    current_dir = c_path
    templates_dir = os.path.join(current_dir, "templates")
    os.makedirs(templates_dir, exist_ok=True)

    template_name = input("Enter a name for your template: ").strip()
    if not template_name:
        print("Template name cannot be empty.")
        return

    alias_map = {
        "whitelist.json": "1) AppArmor whitelist",
        "user_data.json": "2) Selected users",
        "ranked_clients.json": "3) Chosen clients",
        "allowed_domains.json": "4) Domain whitelist",
    }

    json_paths = {}
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith(".json") and file not in ("json_references.json", "user_counts.json"):
                full_path = os.path.join(root, file)
                json_paths[file] = full_path

    if not json_paths:
        print("No valid JSON files found to save.")
        return

    print("Which JSON files would you like to include in the template?")
    for idx, (fname, alias) in enumerate(alias_map.items(), start=1):
        if fname in json_paths:
            print(alias)

    selection = input("Enter the numbers of the files you want to include (e.g. 1 2 3), or type 'exit' to cancel: ").strip().lower()
    if not selection or selection == "exit":
        print("Cancelled.")
        return

    selected_indexes = set(selection.split())
    selected_files = [f for i, f in enumerate(alias_map.keys(), start=1) if str(i) in selected_indexes and f in json_paths]

    if not selected_files:
        print("No valid selections made.")
        return

    template_path = os.path.join(templates_dir, template_name)
    os.makedirs(template_path, exist_ok=True)

    for file in selected_files:
        src_path = json_paths[file]
        dest_path = os.path.join(template_path, file)
        shutil.copy2(src_path, dest_path)
        print(f"Copied {file} to template.")

    print(f"\nTemplate '{template_name}' saved successfully at {template_path}.")

def load_template():
    template_dir = "templates"
    
    if not os.path.exists(template_dir):
        print(f"Template folder '{template_dir}' does not exist.")
        return

    folders = [folder for folder in os.listdir(template_dir) if os.path.isdir(os.path.join(template_dir, folder))]

    if not folders:
        print("No templates found.")
        return

    print("Available templates:")
    for folder in folders:
        print(f"- {folder}")
    print("- exit (cancel)")

    load = input("Enter the name of the template you want to load: ").strip()
    if not load or load.lower() == "exit":
        print("Cancelled.")
        return

    load_path = os.path.join(template_dir, load)
    if not os.path.exists(load_path):
        print(f"Template '{load}' does not exist.")
        return

    file_map = {
        "whitelist.json": f"projects/{current_project_number}/whitelist.json",
        "user_data.json": f"projects/{current_project_number}user_data.json",
        "ranked_clients.json": f"projects/{current_project_number}ranked_clients.json",
        "allowed_domains.json": f"projects/{current_project_number}allowed_domains.json"
    }

    for filename, destination in file_map.items():
        source_file = os.path.join(load_path, filename)
        if os.path.exists(source_file):

            dest_dir = os.path.dirname(destination)
            os.makedirs(dest_dir, exist_ok=True)

            shutil.copy2(source_file, destination)
            print(f"Copied {filename} -> {destination}")
        else:
            print(f"Skipped: {filename} (not found in template)")

    print(f"\nTemplate '{load}' loaded successfully.")

def delete_template():
    template_dir = "templates"

    if not os.path.exists(template_dir):
        print(f"Template folder '{template_dir}' does not exist.")
        return

    folders = [folder for folder in os.listdir(template_dir) if os.path.isdir(os.path.join(template_dir, folder))]

    if not folders:
        print("No templates to delete.")
        return

    print("Available templates:")
    for folder in folders:
        print(f"- {folder}")
    print("- exit (cancel)")

    choice = input("Enter the name of the template you want to delete: ").strip()
    if not choice or choice.lower() == "exit":
        print("Cancelled.")
        return

    target_path = os.path.join(template_dir, choice)
    if not os.path.exists(target_path):
        print(f"Template '{choice}' does not exist.")
        return

    confirm = input(f"Are you sure you want to delete '{choice}'? This cannot be undone! (y/n): ").strip().lower()
    if confirm != 'y':
        print("Deletion cancelled.")
        return

    shutil.rmtree(target_path)
    print(f"Template '{choice}' deleted successfully.")

def template_controller_menu():
    while True:
        print("Select an option:")
        print("1. List templates")
        print("2. Save template")
        print("3. Load template")
        print("4. Delete templates")
        print("5. Exit")

        choice = input("Enter the number of your choice: ").strip()

        if choice == "1":
            list_templates()
        elif choice == "2":
            save_template()
        elif choice == "3":
            load_template()
        elif choice == "4":
            delete_template()

        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    template_controller_menu()

#app_armor_default/whitelist.json, users_default/user_data.json, clients_deafault/ranked_clients.json, unbound_default/allowed_domains.json, clients_default/user_counts.json