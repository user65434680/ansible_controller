#!/usr/bin/env python3

import subprocess
from clients_default.user_count import client_ranking
from clients_default.generate_keys_script import generate_ssh_keys_for_clients
from ansible_utils import run_ansible_playbook
import os

c_path = os.path.dirname(os.path.abspath(__file__))

def assign_computers_manually():
    inventory_file_path = "../inventory/inventory.ini"
    
    if not os.path.exists(inventory_file_path):
        print(f"Inventory file '{inventory_file_path}' does not exist.")
        return

    clients = []
    with open(inventory_file_path, "r") as file:
        in_clients_section = False
        for line in file:
            line = line.strip()
            if line.startswith("[clients]"):
                in_clients_section = True
                continue
            if in_clients_section:
                if line == "" or line.startswith("["):
                    break
                client_name = line.split()[0]
                clients.append(client_name)

    if not clients:
        print("No clients found in the inventory file.")
        return

    print("Select a client:")
    for i, client in enumerate(clients, start=1):
        print(f"{i}) {client}")

def assign_computers_automatically():
    print("Running playbook to echo available computers...")
    run_ansible_playbook(f"{c_path}/echo_available_computers.yml")
    client_ranking()

def add_to_ansible():
    add_choice = input("This is used to add new computers to ansible. You need username, password, IP and openssh-server to be installed.\n"
                       "All computers must have the same sudo password for this to work, so do not add computers with different passwords.\n"
                       "1) continue\n2) exit\n option: ").strip()
    if add_choice == "1":
        add_to_ansible2()
    elif add_choice == "2":
        print("Exiting")
        return

def add_to_ansible2():
    generate_ssh_keys_for_clients()

    ansible_user = input("Enter the computer client username: ").strip()
    ansible_IP = input("Enter the client IP address: ").strip()

    inventory_file_path = "../inventory/inventory.ini"

    with open(inventory_file_path, 'a') as inventory_file:
        inventory_file.write(f"\n[clients]\n{ansible_user} ansible_host={ansible_IP} ansible_user={ansible_user}\n")

    print(f"Client {ansible_user} with IP {ansible_IP} added to the inventory file.")

def assign_computers_choice():
    assign_computers_choice = input("Would you like to either assign computers\n1) manually\n2) automatically\n3) Exit\nSelect number: ").strip()
    if assign_computers_choice == "1":
        assign_computers_manually()
    elif assign_computers_choice == "2":
        assign_computers_automatically()
    elif assign_computers_choice == "3":
        print("Exiting.")
        return
    else:
        print("Please choose again.")

def client_control_menu():
    while True:
        print("\nClient Control Menu:")
        print("1) Assign computers")
        print("2) Add to Ansible")
        print("3) Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            assign_computers_choice()
        elif choice == "2":
            add_to_ansible()
        elif choice == "3":
            print("Exiting.")
            return
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    client_control_menu()