#!/usr/bin/env python3

import json
import sys
import os
import subprocess
from users_default.random_gen import generate_random_password
from ansible_utils import run_ansible_playbook
from projects.project_context import get_current_project_number
from copy_controller import copy_file, delete_file

current_project_number = get_current_project_number()

c_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(c_path)
projects_path = os.path.join(root_path, "projects")

user_data_file = os.path.join(projects_path, current_project_number, "user_data.json")


def add_users_from_file():
    filename = input("Enter the file name that contains names from students. (only works as .txt)").strip()
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
            
        with open(user_data_file, 'w') as file:
            json.dump({'users': users}, file, indent=4)

        print("Users have been added to users_default/user_data.json.")
        
    except FileNotFoundError:
        print(f"file {filename} not found")
    except Exception as e:
        print(f"An error occurred: {e}")

def add_user():
    global user_data

    if user_data['users']:
        print("\nThere are already users in the list. Choose an option:")
        print("1) Add more users")
        print("2) Clear contents and add new users")
        print("3) Clear contents")
        print("4) Exit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            pass
        elif choice == "2":
            user_data['users'] = []
        elif choice == "3":
            user_data['users'] = []
            with open(user_data_file, 'w') as file:
                json.dump(user_data, file, indent=4)
            print("Contents cleared.")
            return
        elif choice == "4":
            print("Exiting.")
            return
        else:
            print("Invalid choice. Exiting.")
            return

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

    with open(user_data_file, 'w') as file:
        json.dump(user_data, file, indent=4)

    print("Users have been added to users_default/user_data.json.")

def user_control():

    global user_data
    
    try:
        with open(user_data_file, 'r') as file:
            user_data = json.load(file) or {'users': []}
    except FileNotFoundError:
        user_data = {'users': []}

    option = input("User control options:\n1) Push user to client\n2) Create new user\n3) create new user from txt file\n4) Delete user\n5) Exit\nSelect an option: ").strip()

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
    copy_file("user_data.json")
    run_ansible_playbook(f"{c_path}/del_users.yml")
    delete_file("user_data.json")

def push_user():
    copy_file("user_data.json")
    run_ansible_playbook(f"{c_path}/users.yml")
    delete_file("user_data.json")

if __name__ == '__main__':
    user_control()