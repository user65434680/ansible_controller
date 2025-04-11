#!/usr/bin/env python3

import subprocess
import sys
import yaml
import random
import string

def run_ansible_playbook(playbook, ask_become_pass=False):
    command = ['ansible-playbook', '-i', 'inventory.ini', playbook]
    
    if ask_become_pass:
        command.append('--ask-become-pass')
    
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
        print(f"Playbook {playbook} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running playbook {playbook}: {e.stderr}")

def add_user():
    global user_data
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

    with open('user_data.yml', 'w') as file:
        yaml.dump(user_data, file, default_flow_style=False)

    print("Users have been added to user_data.yml.")
    run_ansible_playbook('users.yml', ask_become_pass=False)

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + "!?"
    return ''.join(random.choice(characters) for _ in range(length))

def delete_user():
    run_ansible_playbook('del_users.yml')

def create_user():
    run_ansible_playbook('users.yml')

def main():
    global user_data
    
    try:
        with open('user_data.yml', 'r') as file:
            user_data = yaml.safe_load(file) or {'users': []}
    except FileNotFoundError:
        user_data = {'users': []}

    print("Select an option:")
    print("1. Create user")
    print("2. Delete user")
    print("3. Add users interactively")

    choice = input("Enter the number of your choice: ").strip()

    if choice == "1":
        create_user()
    elif choice == "2":
        delete_user()
    elif choice == "3":
        add_user()
    else:
        print("Invalid choice. Exiting.")

if __name__ == '__main__':
    main()
