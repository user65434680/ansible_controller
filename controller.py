#!/usr/bin/env python3

import subprocess
import sys
import os
import json
from random_gen import generate_random_password
from clients import client_ranking
from generate_keys_script import generate_ssh_keys_for_clients
from domain_controller import choose_action

def run_ansible_playbook(playbook, ask_become_pass=False):
    command = ['ansible-playbook', '-i', 'inventory.ini', playbook, '--ask-become-pass']
    
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
        print(f"Playbook {playbook} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running playbook {playbook}: {e.stderr}")

def add_users_from_file():
    filename = input ("Enter the file name that contains names from students. (only works as .txt)").strip()
    try:
        with open(filename, 'r') as file:
            users = []
            for line in file:
                names = line.strip().split()
                if len(names) == 2:
                    firstname, lastname = names[0], names[1]

                    username = (firstname[:3] + lastname[:3]).lower()

                    password = generate_random_password()

                    users.append({'username': username, 'password': password})
            
        with open('user_data.json', 'w') as file:
            json.dump({'users': users}, file, indent=4)

        print("Users have been added to user_data.json.")
        
    except FileNotFoundError:
        print(f"file {filename} not found")
    except Exception as e:
        print(f"An error occured {e}")


def add_user():
    print("\n--- Adding Users ---")
    while True:
        username = input("Enter username (or type 'exit' to stop): ").strip()
        if username.lower() == 'exit':
            break

        password_choice = input("Would you like to either\n1) Enter passwords manually\n2) Generate a random password automatically (8 characters)?\nChoose 1 or 2: ").strip()

        if password_choice == "1":
            password = input("Enter password: ").strip()
        elif password_choice == "2":
            password = generate_random_password()
        else:
            print("Invalid choice. Try again.")
            continue

        user_data['users'].append({
            'username': username,
            'password': password
        })

        print(f"User '{username}' has been added.")

    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)

    print("Users have been added to user_data.json.")

def user_control():

    option = input("User control options:\n1) Push user to client\n2) Create new user\n3) create new user from txt file\n4) Delete user\n5) Exit").strip()

    if option == "1":
        push_user()
    elif option == "2":
        add_user() 
    elif option == "3":
        add_users_from_file()
    elif option == "4":
        delete_user()
    elif option == "5":
        return


def delete_user():
    run_ansible_playbook('del_users.yml')


def push_user():
    run_ansible_playbook('users.yml')

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

    add_choice = input("This is used to add new computers to ansible using username, password, IP and openssh-server to be installed.\n all computers must have the same password for this to work so do not add computers with different passwords.\n1) continue\n2) exit\n number:")

    if add_choice == "1":
        add_to_ansible2()
    elif add_choice =="2":
        print("exiting")
        return
        
def add_to_ansible2():

    generate_ssh_keys_for_clients()

    playbook_1 = "add_computer.yml"
    ansible_user = input("Enter the computer client username: ").strip()
    ansible_IP = input("Enter the client IP address: ").strip()

    with open('inventory.ini', 'a') as inventory_file:
        inventory_file.write(f"\n[clients]\n{ansible_user} ansible_host={ansible_IP} ansible_user={ansible_user}\n")

    ansible_1 = ['ansible-playbook', '-i', ansible_IP, playbook_1, '-u', ansible_user, '--ask-become-pass']

    try:
        result = subprocess.run(ansible_1, check=True, text=True, capture_output=True)
        print(result.stdout)
        print(f"Playbook {playbook_1} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running playbook {playbook_1}: {e.stderr}")

def assign_computers_choice():
    
    assign_computers_choice = input("Would you like to either assign computers\n1) manually\n2) automatically\n").strip()

    if assign_computers_choice == "1":
        assign_computers_manually()
    elif assign_computers_choice == "2":
        assign_computers_automatically()
    else:
        print ("please choose again")

def main():
    global user_data
    
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file) or {'users': []}
    except FileNotFoundError:
        user_data = {'users': []}

    while True:
        print("Select an option:")
        print("1. User control")
        print("2. Assign target computers")
        print("3. Exit")
        print("4. Domains")
        print("5. Add a client to ansible")

        choice = input("Enter the number of your choice: ").strip()



        if choice == "1":
            user_control
        elif choice == "2":
            assign_computers_choice()
        elif choice == "3":
            choose_action()
        elif choice == "4":
            add_to_ansible()
        elif choice == "5":

            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    main()
