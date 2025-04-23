#!/usr/bin/env python3

import os
import subprocess
import sys

from ansible_utils import run_ansible_playbook
from copy_controller import copy_file, delete_file

from projects.project_context import get_current_project_number

current_project_number = get_current_project_number()

file_map = {
    "whitelist.json": f"projects/{current_project_number}/whitelist.json",
    "user_data.json": f"projects/{current_project_number}/user_data.json",
    "custom_clients.ini": f"projects/{current_project_number}/custom_clients.ini",
    "allowed_domains.json": f"projects/{current_project_number}/allowed_domains.json",
}

alias_map = {
    "whitelist.json": "AppArmor whitelist",
    "user_data.json": "Selected users",
    "custom_clients.ini": "Chosen clients",
    "allowed_domains.json": "Domain whitelist",
}

yml_map = {
    # apparmor
    "create_blacklist.yml": "apparmor_default",
    "delete_blacklist.yml": "apparmor_default",
    "remove_whitelist.yml": "apparmor_default",
    "whitelist_apps.yml": "apparmor_default",
    # unbound
    "unbound_clear_blacklist.yml": "unbound_default",
    "unbound_clear_domains.yml": "unbound_default",
    "unbound_whitelist.yml": "unbound_default",
    # users
    "del_users.yml": "users_default",
    "delete_all_users.yml": "users_default",
    "users.yml": "users_default",
}

selection_map = {
    "1": {
        "desc": "Pushing AppArmor whitelist...",
        "json_file": "whitelist.json",
        "yml_file": "whitelist_apps.yml",
    },
    "2": {
        "desc": "Pushing selected users...",
        "json_file": "user_data.json",
        "yml_file": "users.yml",
    },
    "3": {
        "desc": "Pushing domain whitelist...",
        "json_file": "allowed_domains.json",
        "yml_file": "unbound_whitelist.yml",
    }
}

correlating_files_map = {
    "user_data.json": "users.yml",
    "allowed_domains.json": "unbound_whitelist.yml",
    "whitelist.json": "whitelist_apps.yml",
}

def check_list():
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

def push_menu():
    while True:
        check_list()
        if not os.path.isfile(file_map["custom_clients.ini"]):
            print("WARNING: Custom client selection not found. Please consider creating one to prevent pushing changes to all clients on the network.")

        choose_main = input("Would you like to push from pending changes or from checklist?\n1. checklist\n2. pending changes\n3. exit\n").strip()

        if choose_main == "1":
            available_options = [
                key for key, value in file_map.items() if os.path.isfile(value)
            ]

            if available_options:
                print("\nAvailable options:")
                option_map = {}
                for idx, key in enumerate(available_options, start=1):
                    print(f"{idx}. {alias_map.get(key, key)}")
                    option_map[idx] = key
                print(f"{len(available_options) + 1}. Exit")
            else:
                print("No configuration files found. Please complete configuration first.")
                continue

            selection = input("\nPlease choose what to push to clients: ").strip()

            try:
                selection_idx = int(selection)
                if selection_idx in option_map:
                    selected_key = option_map[selection_idx]
                    json_file_path = file_map[selected_key]
                    json_file_name = os.path.basename(json_file_path)
                    yml_file_name = correlating_files_map[selected_key]
                    yml_file_path = os.path.join(yml_map[yml_file_name], yml_file_name)

                    print(f"Running corresponding file for: {alias_map.get(selected_key, selected_key)}")
                    copy_file(json_file_name)
                    run_ansible_playbook(yml_file_path)
                    delete_file(json_file_name)

                elif selection_idx == len(available_options) + 1:
                    print("Exiting")
                    sys.exit()
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choose_main == "2":
            print("1. placeholder for pending changes")
        elif choose_main == "3":
            print("Exiting")
            return