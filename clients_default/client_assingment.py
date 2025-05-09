#!/usr/bin/env python3

from ansible_utils import run_ansible_playbook
import os

from clients_default.assing_computers_automatically import client_ranking_from_inventory
c_path = os.path.dirname(os.path.abspath(__file__))

def assign_computers_manually(inventory_file="inventory/inventory.ini"):
    """Display clients from the inventory file and allow the user to select."""
    if not os.path.exists(inventory_file):
        print(f"Error: Inventory file '{inventory_file}' not found.")
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

    print("Select a client:")
    for i, client in enumerate(clients, start=1):
        print(f"{i}) {client}")

    try:
        selection = int(input("\nEnter the number of the client you want to select: ").strip())
        if 1 <= selection <= len(clients):
            selected_client = clients[selection - 1]
            print(f"You selected: {selected_client}")
        else:
            print("Invalid selection. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def assign_computers_automatically():
    run_ansible_playbook(f"{c_path}/echo_available_computers.yml")
    client_ranking_from_inventory()