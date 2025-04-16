#!/usr/bin/env python3

from users_default.user_controller import user_control
from unbound_default.domain_controller import choose_action
from clients_default.client_control import client_control_menu
from apparmor_default.app_armor_controller import app_armor_menu

def main():
    while True:
        print("Select an option:")
        print("1. Users")
        print("2. Client computers")
        print("3. Domains")
        print("4. AppArmor")
        print("5. Exit")

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
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()
