#!/usr/bin/env python3

import os
import subprocess
import sys

from ansible_utils import run_ansible_playbook
from copy_controller import copy_file, delete_file

from projects.project_context import get_current_project_number

current_project_number = get_current_project_number()

file_map = {
    "allowed_domains.json": f"projects/{current_project_number}/allowed_domains.json",
    "whitelist.json": f"projects/{current_project_number}/whitelist.json",
    "user_data.json": f"projects/{current_project_number}/user_data.json",
    "custom_clients.ini": f"projects/{current_project_number}/custom_clients.ini",
}

alias_map = {
    "whitelist.json": "1. AppArmor whitelist",
    "user_data.json": "2. Selected users",
    "custom_clients.ini": "3. Chosen clients",
    "allowed_domains.json": "4. Domain whitelist",
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
            print("1. AppArmor whitelist")
            print("2. Selected users")
            print("3. Domain whitelist")
            print("4. Chosen clients")
            print("5. Exit")


            selection = input("\nPlease choose what to push to clients: ").strip()

            if selection in selection_map:
                task = selection_map[selection]
                print(task["desc"])
                copy_file(task["json_file"])

                yml_dir = yml_map[task["yml_file"]]
                full_playbook_path = f"{yml_dir}/{task['yml_file']}"

                run_ansible_playbook(full_playbook_path)
                delete_file(task["json_file"])

            elif selection == "4":
                print("Selected custom clients for operation.")
                print("PLACEHOLDER REMEMBER TO MAKE INTO A VARIABLE FOR RUNNING THE PLAYBOOK TO SPECIFIC CLIENTS!!!")

            elif selection == "5":
                print("Exiting")
                sys.exit()

            else:
                print("Invalid selection. Please try again.")
                return

        elif choose_main == "2":
            print("1. placeholder for pending changes")
