#!/usr/bin/env python3

from users_default.user_controller import user_control
from unbound_default.domain_controller import choose_action
from clients_default.client_control import client_control_menu
from templates.template_controller import template_controller_menu
import subprocess
import sys
from push_changes import push_menu
from setup_wizard import start_wizard




def main_menu():
    while True:
        print("Select an option:")
        print("1. Easy setup wizard")
        print("2. Users")
        print("3. Client computers")
        print("4. Domains")
        print("5. Templates")
        print("6. Push changes to client")
        print("7. Return to projects")
        print("8. Exit the system")

        choice = input("Enter the number of your choice: ").strip()

        if choice == "1":
            start_wizard()
        elif choice == "2":
            user_control()
        elif choice == "3":
            client_control_menu()
        elif choice == "4":
            choose_action()
        elif choice == "5":
            template_controller_menu()
        elif choice == "6":
            push_menu()
        elif choice == "7":
            print("Exiting to projects...")
            subprocess.run(["python3", "run.py"])
            sys.exit()

        elif choice == "8":
            exit_choice = input("If you exit some changes may not be saved. Are you sure you want to exit?\ntype: yes or no\n").strip()
                
            if exit_choice == "yes":
                print("Exiting the program.")
                break
            elif exit_choice == "no":
                print("Returning to main menu.")
                continue
            else:
                print("Invalid input please type yes or no.")

            
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
