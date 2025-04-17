#!/usr/bin/env python3

import os 
import sys
import subprocess
import json
from ansible_utils import run_ansible_playbook
from projects.project_context import get_current_project_number

current_project_number = get_current_project_number()

c_path = os.path.dirname(os.path.abspath(__file__))
projects = os.path.join(c_path, "projects")
a_path = os.path.dirname(projects)
def generate_profile(path):
    return f"""#include <tunables/global>

{path} {{
  {path} rix,
}}
"""

#segment 1 whitelist
WHITELIST_FILE = os.path.join(a_path, current_project_number, "whitelist.json")

def load_whitelist():
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, "r") as f:
            return json.load(f)
    return []

def save_whitelist(data):
    with open(WHITELIST_FILE, "w") as f:
        json.dump(data, f, indent=2)

def main_1():
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
        whitelist.append({
            "name": name,
            "path": path,
            "profile": profile
        })
        print(f"Added {path} to whitelist.")

    save_whitelist(whitelist)
    print(f"\nSaved to {WHITELIST_FILE}")



def control_whitelist():

    data1 = input("choose\n1) add to whitelist\n2) remove from whitelist\n3) exit\n").strip()

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

# segment2 blacklist
def control_blacklist():
    
    data2 = input("choose\n1) create blacklist and deny all apps\n2) remove blacklist disable all apps\n3) exit\n").strip()

    if data2 == "1":
        print("placeholder")



def app_armor_menu():

    print("AppArmor Menu")
    print("1. Control whitelist")
    print("2. Control blacklist")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        control_whitelist()
    elif choice == '2':
        control_blacklist()
    elif choice == '3':
        return
    else:
        print("Invalid choice. Please try again.")
        app_armor_menu()
    

if __name__ == "__main__":
    app_armor_menu()