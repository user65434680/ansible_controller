#!/usr/bin/env python3

from users_default.user_controller import user_control
from unbound_default.domain_controller import choose_action
from clients_default.client_control import client_control_menu
from apparmor_default.app_armor_controller import app_armor_menu
from template_controller import template_controller_menu
import subprocess
import sys




def main_menu():
    while True:
        print("Select an option:")
        print("1. Users")
        print("2. Client computers")
        print("3. Domains")
        print("4. AppArmor")
        print("5. Templates")
        print("6. Return to projects")
        print("7. Exit the system")

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
            print("Exiting to projects...")
            subprocess.run(["python3", "run_this.py"])
            sys.exit()

        elif choice == "7":
            exit_choice = input("If you exit some changes may not be saved. Are you sure you want to exit?\n type: yes or no\n").strip()
                
            if exit_choice == "yes":
                print("Exiting the program.")
                break
            elif exit_choice == "no":
                return
            else:
                print("Invalid input please type yes or no.")

            
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
