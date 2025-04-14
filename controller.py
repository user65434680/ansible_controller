#!/usr/bin/env python3

import subprocess
import sys
import json
from random_gen import generate_random_password
from clients import client_ranking

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


def delete_user():
    run_ansible_playbook('del_users.yml')


def create_user():
    run_ansible_playbook('users.yml')

def assign_computers_manually():
    with open("clients.txt", "r") as file:
        clients = [line.strip() for line in file if line.strip()]

    print("Select a client:")
    for i, client in enumerate(clients, start=1):
        print(f"{i}) {client}")

def assing_computers_automatically():
    run_ansible_playbook('echo_available_computers.yml')
    client_ranking


def assing_computers_choice():
    
    assing_computers_choice = input("Would you like to either assing computers\n manually\n1) automatically\n2)").strip()

    if assing_computers_choice == "1":
        assign_computers_manually
    elif assing_computers_choice == "2":
        assing_computers_automatically


def main():
    global user_data
    
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file) or {'users': []}
    except FileNotFoundError:
        user_data = {'users': []}

    while True:
        print("Select an option:")
        print("1. Create user")
        print("2. Delete user")
        print("3. Add users interactively")
        print("4. Add users from txt file")
        print("5. assing target computers")
        print("6. Exit")

        choice = input("Enter the number of your choice: ").strip()

        if choice == "1":
            create_user()
        elif choice == "2":
            delete_user()
        elif choice == "3":
            add_user()
        elif choice == "4":
            add_users_from_file()
        elif choice == "5":
            assing_computers_choice
        elif choice == "6":

            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    main()
