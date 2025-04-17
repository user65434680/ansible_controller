#!/usr/bin/env python3

from users_default.user_controller import user_control
from unbound_default.domain_controller import choose_action
from clients_default.client_control import client_control_menu
from apparmor_default.app_armor_controller import app_armor_menu
from template_controller import template_controller_menu
from project_manager import ensure_projects_folder, list_projects, create_project, load_project

def start():
    ensure_projects_folder()
    print("\nWelcome to the system configuration tool.")
    print("Please select an option from the menu.")
    print("1. Create project")
    print("2. Load project")
    print("3. List projects")
    print("4. Exit")

    choice = input("Choice: ").strip()
    if choice == "1":
        create_project()
    elif choice == "2":
        current_project_number = load_project()
        if current_project_number:
            print(f"Switching to main menu for project {current_project_number}...\n")
            main_menu()
    elif choice == "3":
        list_projects()
    elif choice == "4":
        print("Exiting.")
    else:
        print("Invalid choice.")

def main_menu():
    while True:
        print("Select an option:")
        print("1. Users")
        print("2. Client computers")
        print("3. Domains")
        print("4. AppArmor")
        print("5. Templates")
        print("6. Exit")

        choice = input("Enter the number of your choice: ").strip()

        if choice == "1":
            user_control()
        elif choice == "2":
            client_control_menu()
        elif choice == "3":
            choose_action()
        elif choice == "4":
            app_armor_menu()
        elif choice == "5":
            template_controller_menu()
        elif choice == "6":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    start()
