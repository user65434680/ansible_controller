#!/usr/bin/env python3

import os
import subprocess
import json
import json
import os
from projects.project_context import get_current_project_number
from projects.pending_control.py import add_to_pending

current_project_number = get_current_project_number()

c_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(c_path)
projects_path = os.path.join(root_path, "projects")
allowed_domains_file = os.path.join(projects_path, current_project_number, "allowed_domains.json")  # Correct path

def allow_domains():
    ensure_allowed_domains_file()
    existing_domains = {"domains": []}

    if os.path.exists(allowed_domains_file) and os.path.getsize(allowed_domains_file) > 0:
        try:
            with open(allowed_domains_file, 'r') as file:
                data = json.load(file)

                if isinstance(data, dict) and "domains" in data and isinstance(data["domains"], list):
                    existing_domains = data
                else:
                    print("Invalid structure in allowed_domains.json. Resetting to default.")
        except json.JSONDecodeError:
            print("Corrupt JSON in allowed_domains.json. Resetting to default.")

    print("Type allowed domains (like youtube.com). Type 'continue' to finish and apply changes.\n")

    while True:
        domain = input("Enter domain: ").strip()

        if domain.lower() == "continue":
            break

        if not domain:
            print("Domain cannot be empty. Try again.")
            continue

        if domain in existing_domains["domains"]:
            print(f"'{domain}' is already in the list.")
        else:
            existing_domains["domains"].append(domain)
            print(f"Added '{domain}' to allowed domains.")

    with open(allowed_domains_file, 'w') as file:
        json.dump(existing_domains, file, indent=4)

    print("Allowed domains updated. To push this change to clients please go to main menu and select push changes.")

def ensure_allowed_domains_file():
    """Ensure that allowed_domains.json exists. If not, create it with a default structure."""
    if not os.path.exists(allowed_domains_file):
        print(f"{allowed_domains_file} does not exist. Creating it...")
        os.makedirs(os.path.dirname(allowed_domains_file), exist_ok=True)
        with open(allowed_domains_file, 'w') as file:
            json.dump({"domains": []}, file, indent=4)
        print(f"{allowed_domains_file} has been created with a default structure.")

def clear_allowed_domains():
    with open(allowed_domains_file, 'w') as file:
        json.dump([], file, indent=4)
    add_to_pending(projects_path, current_project_number, "domain_changes", "unboud_clear_domains.yml")


def clear_all():

    with open('allowed_domains.json', 'w') as file:
        json.dump([], file, indent=4)
    add_to_pending(projects_path, current_project_number, "domain_changes", "unbound_clear_blacklist")

def choose_action():
    while True:
        print("Select an option:")
        print("1. Allow domains")
        print("2. Clear allowed domains")
        print("3. Clear all domains and blacklist")
        print("4. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            allow_domains()
        elif choice == "2":
            clear_allowed_domains()
        elif choice == "3":
            clear_all()
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    choose_action()
