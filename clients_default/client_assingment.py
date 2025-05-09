#!/usr/bin/env python3

import os

c_path = os.path.dirname(os.path.abspath(__file__))

def assign_computers_manually():
    """Display clients from the inventory file and allow the user to select."""
    inventory_file = os.path.join(os.path.dirname(c_path), "inventory", "inventory.ini")

    if not os.path.exists(inventory_file):
        print(f"Error: Inventory file '{inventory_file}' not found.")
        return

    clients = []
    with open(inventory_file, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("[clients]"):
                continue
            if line:
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