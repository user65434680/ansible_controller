#!/usr/bin/env python3

import json
import os
from projects.project_context import get_current_project_number

current_project_number = get_current_project_number()

c_path = os.path.dirname(os.path.abspath(__file__))
projects_path = os.path.join(os.path.dirname(c_path), "projects")
user_counts_file = os.path.join(c_path, "user_counts.json")
custom_clients_file = os.path.join(projects_path, current_project_number, "custom_clients.ini")

def load_user_counts(path=user_counts_file):
    with open(path, "r") as f:
        return json.load(f)

def client_ranking():
    try:
        num_needed = int(input("How many computers are needed? "))
    except ValueError:
        print("Please enter a valid number.")
        return
    
    try:
        user_counts = load_user_counts()
    except FileNotFoundError:
        print(f"Error: {user_counts_file} not found.")
        return

    all_clients = {k: v for k, v in user_counts.items() if k.startswith("client") and k[6:].isdigit()}

    sorted_clients = sorted(
        all_clients.items(),
        key=lambda item: (item[1], extract_client_number(item[0]))
    )

    chosen_clients = sorted_clients[:num_needed]

    print("\nSelected Clients:")
    for name, count in chosen_clients:
        print(f"{name}: {count} users")

    ini_content = "[clients]\n"
    ini_content += "\n".join(f"{name} ansible_host={name}.example.com" for name, _ in chosen_clients)

    ini_file_path = os.path.join(projects_path, current_project_number, "custom_clients.ini")
    with open(ini_file_path, "w") as f:
        f.write(ini_content)

    print(f"\nSaved selected clients to '{ini_file_path}'.")

def extract_client_number(name):
    return int(name.replace("client", ""))

if __name__ == "__main__":
    client_ranking()