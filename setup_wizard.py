#!/usr/bin/env python3

import os
import json

from users_default.user_controller import add_user
from users_default.user_controller import user_control
from users_default.user_controller import add_users_from_file
from clients_default.client_control import assign_computers_choice
from clients_default.client_assingment import assign_computers_manually
from clients_default.client_control import assign_computers_automatically
from unbound_default.domain_controller import allow_domains
from clients_default.client_control import add_to_ansible


def start_wizard():
    print("Setup wizard is used to guide you through configuration in the right order.")
    choice = input("Press 1 to start 2 to exit: ").strip()
    if choice == "1":
        print("Starting setup wizard...")
        wizard()
    elif choice == "2":
        print("Exiting setup wizard.")
    else:
        print("Invalid input. Please enter 1 or 2.")
def wizard():
    while True:
        print("Welcome to the wizard. You can exit at any time by typing 'exit'.")
        
        choice = input("Would you like to add new clients to ansible? This adds them to the control environment BUT these aren't the computers you will be pushing to.\n1. yes\n2. no\n").strip()
        if choice == "exit":
            break
        elif choice == "1":
            add_to_ansible()
        elif choice == "2":
            pass
        else:
            print("Invalid input. Please enter 1 or 2.")
            continue
        choice = input("Please select how you would like to select clients you are going to push to.\n1. Manually\n2. Automatically\n3. skip (not recommended)\n").strip()
        if choice == "exit":
            break
        elif choice == "1":
            assign_computers_manually()
        elif choice == "2":
            assign_computers_automatically()
        elif choice == "3":
            print("Skipping...")
        else:
            print("Invalid input. Please enter 1, 2.or 3")
            continue

        choice = input("Please select how you would like to add users.\n1. Add users\n2. skip\n").strip()
        if choice == "exit":
            break
        elif choice == "1":
            user_control()
        elif choice == "2":
            print("Skipping...")
        else:
            print("Invalid input. Please enter 1 or 2.")
            continue

        choice = input("Would you like to add whitelisted websites?\n1. yes\n2. no\n").strip()
        if choice == "exit":
            break
        elif choice == "1":
            allow_domains()
        elif choice == "2":
            pass
        else:
            print("Invalid input. Please enter 1 or 2.")
            continue

        print("Setup wizard complete. You can now push changes to clients.")
        break
