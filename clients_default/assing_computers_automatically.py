#!/usr/bin/env python3

import json
import os
from projects.project_context import get_current_project_number

current_project_number = get_current_project_number()

c_path = os.path.dirname(os.path.abspath(__file__))
projects_path = os.path.join(os.path.dirname(c_path), "projects")
user_counts_file = os.path.join(c_path, "user_counts.json")
custom_clients_file = os.path.join(projects_path, current_project_number, "custom_clients.ini")

def client_ranking_from_inventory(inventory_file="inventory/inventory.ini"):
    """Automatically assign clients from the inventory file."""
    if not os.path.exists(inventory_file):
        print(f"Error: Inventory file '{inventory_file}' not found.")
        return

    try:
        num_needed = int(input("How many computers are needed? "))
    except ValueError:
        print("Please enter a valid number.")
        return

    clients = []
    with open(inventory_file, "r") as file:
        in_clients_section = False
        for line in file:
            line = line.strip()
            if line.startswith("[clients]"):
                in_clients_section = True
                continue
            if in_clients_section:
                if line == "" or line.startswith("["): 
                    break
                clients.append(line)

    if not clients:
        print("No clients found in the inventory file.")
        return

    selected_clients = clients[:num_needed]

    ini_content = "[clients]\n"
    ini_content += "\n".join(selected_clients)

    ini_file_path = os.path.join(projects_path, current_project_number, "custom_clients.ini")
    with open(ini_file_path, "w") as f:
        f.write(ini_content)

    print("\nSelected Clients:")
    for client in selected_clients:
        print(client)

    print(f"\nSaved selected clients to '{ini_file_path}'.")