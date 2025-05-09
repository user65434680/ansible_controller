#!/usr/bin/env python3

import os
import subprocess
import sys
import json
from ansible_utils import run_ansible_playbook
from copy_controller import copy_file, delete_file
import shutil


from projects.project_context import get_current_project_number
c_path = os.path.dirname(os.path.abspath(__file__))
current_project_number = get_current_project_number()
certs_path = f"projects/{current_project_number}"

file_map = {
    "user_data.json": f"projects/{current_project_number}/user_data.json",
    "custom_clients.ini": f"projects/{current_project_number}/custom_clients.ini",
    "allowed_domains.json": f"projects/{current_project_number}/allowed_domains.json",
    "certificates": f"{certs_path}"
}

alias_map = {
    "user_data.json": "Selected users",
    "custom_clients.ini": "Chosen clients",
    "allowed_domains.json": "Domain whitelist",
    "certificates": "certificates"
}

yml_map = {
    "unbound_clear_blacklist.yml": "unbound_default",
    "unbound_clear_domains.yml": "unbound_default",
    "unbound_whitelist.yml": "unbound_default",
    "del_users.yml": "users_default",
    "delete_all_users.yml": "users_default",
    "users.yml": "users_default",
}

selection_map = {
    "1": {
        "desc": "Pushing selected users...",
        "json_file": "user_data.json",
        "yml_file": "users.yml",
    },
    "2": {
        "desc": "Pushing domain whitelist...",
        "json_file": "allowed_domains.json",
        "yml_file": "unbound_whitelist.yml",
    }
}

correlating_files_map = {
    "user_data.json": "users.yml",
    "allowed_domains.json": "unbound_whitelist.yml",
}

def check_list():
    """Display files that are done and not yet completed."""
    done = []
    not_done = []

    for name, path in file_map.items():
        if os.path.isfile(path):
            done.append(name)
        else:
            not_done.append(name)

    print("Done:")
    for item in done:
        print(f" - {alias_map.get(item, item)}")

    print("\nNot done yet:")
    for item in not_done:
        print(f" - {alias_map.get(item, item)}")

def push_from_checklist():
    """Handle pushing from checklist."""
    available_options = [
        key for key, value in file_map.items() if os.path.isfile(value)
    ]

    if not available_options:
        print("No configuration files found. Please complete configuration first.")
        return

    print("\nAvailable options:")
    option_map = {}
    for idx, key in enumerate(available_options, start=1):
        print(f"{idx}. {alias_map.get(key, key)}")
        option_map[idx] = key
    print(f"{len(available_options) + 1}. Exit")

    try:
        selection = int(input("\nPlease choose what to push to clients: ").strip())
        if selection in option_map:
            selected_key = option_map[selection]
            json_file_name = os.path.basename(file_map[selected_key])
            yml_file_name = correlating_files_map[selected_key]
            yml_file_path = os.path.join(yml_map[yml_file_name], yml_file_name)

            print(f"Running corresponding file for: {alias_map.get(selected_key, selected_key)}")
            copy_file(json_file_name)
            run_ansible_playbook(yml_file_path)

            if selected_key == "allowed_domains.json":
                print("Cloning certs_path to certificates...")
                certificates_dir = os.path.join(c_path, "certificates")
                destination_dir = certificates_dir
                os.makedirs(certificates_dir, exist_ok=True)

                if os.path.exists(certs_path):
                    shutil.copytree(certs_path, destination_dir, dirs_exist_ok=True)
                    print(f"Copied certs directory from '{certs_path}' to '{destination_dir}'.")
                else:
                    print(f"Error: Source certs directory '{certs_path}' does not exist.")

                print("Running certificates/copy_certificates.yml...")
                run_ansible_playbook(f"{c_path}/certificates/copy_certificate.yml")
                run_ansible_playbook(f"{c_path}/certificates/certificate_client.yml")

            delete_file(json_file_name)
        elif selection == len(available_options) + 1:
            print("Exiting")
        else:
            print("Invalid selection. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def push_from_delete_changes():
    """Handle pushing from delete changes."""
    delete_options = {
        key: value for key, value in yml_map.items()
        if key not in ["unbound_whitelist.yml", "users.yml"]
    }

    print("\nDelete Changes Options:")
    option_map = {}
    idx = 1
    for yml_file, folder in delete_options.items():
        print(f"{idx}. {yml_file}")
        option_map[idx] = os.path.join(folder, yml_file)
        idx += 1
    print(f"{idx}. Exit")

    try:
        choose_option = int(input("\nSelect what changes to delete: ").strip())
        if choose_option in option_map:
            yml_file_path = option_map[choose_option]
            print(f"Running playbook: {yml_file_path}")
            run_ansible_playbook(yml_file_path)
        elif choose_option == idx:
            print("Exiting delete changes menu.")
        else:
            print("Invalid selection. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def push_menu():
    """Main push menu that allows users to choose options."""
    check_list()

    while True:
        if not os.path.isfile(file_map["custom_clients.ini"]):
            print("WARNING: Custom client selection not found. Please consider creating one.")

        choose_main = input(
            "Would you like to push from delete changes or from checklist?\n"
            "1. checklist\n2. delete changes\n3. Show checklist\n4. exit\n"
        ).strip()

        if choose_main == "1":
            push_from_checklist()
        elif choose_main == "2":
            push_from_delete_changes()
        elif choose_main == "3":
            check_list()
        elif choose_main == "4":
            print("Exiting")
            return
        else:
            print("Invalid option, please try again.")