#!/usr/bin/env python3


import subprocess
from clients_default.user_count import client_ranking
from clients_default.generate_keys_script import generate_ssh_keys_for_clients
from ansible_utils import run_ansible_playbook

def assign_computers_manually():
    with open("clients.txt", "r") as file:
        clients = [line.strip() for line in file if line.strip()]

    print("Select a client:")
    for i, client in enumerate(clients, start=1):
        print(f"{i}) {client}")

def assign_computers_automatically():
    run_ansible_playbook('echo_available_computers.yml')
    client_ranking

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

    playbook_1 = "add_computer.yml"
    ansible_user = input("Enter the computer client username: ").strip()
    ansible_IP = input("Enter the client IP address: ").strip()

    inventory_file_path = "../inventory/inventory.ini"

    with open(inventory_file_path, 'a') as inventory_file:
        inventory_file.write(f"\n[clients]\n{ansible_user} ansible_host={ansible_IP} ansible_user={ansible_user}\n")

    ansible_1 = ['ansible-playbook', '-i', inventory_file_path, playbook_1, '-u', ansible_user, '--ask-become-pass']

    try:
        result = subprocess.run(ansible_1, check=True, text=True, capture_output=True)
        print(result.stdout)
        print(f"Playbook {playbook_1} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running playbook {playbook_1}: {e.stderr}")

def assign_computers_choice():
    assign_computers_choice = input("Would you like to either assign computers\n1) manually\n2) automatically\nSelect number: \n").strip()
    if assign_computers_choice == "1":
        assign_computers_manually()
    elif assign_computers_choice == "2":
        assign_computers_automatically()
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