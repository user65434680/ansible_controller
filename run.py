#!/usr/bin/env python3

from project_manager import ensure_projects_folder, list_projects, create_project, load_project, delete_project
import subprocess
import os
import sys

def start():
    ensure_projects_folder()
    controller_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "controller.py")
    
    while True:
        print("\nWelcome to the system configuration tool.")
        print("Please select an option from the menu.")
        print("1. Create project")
        print("2. Load project")
        print("3. List projects")
        print("4. Delete project")
        print("5. Exit")

        choice = input("Choice: ").strip()
        if choice == "1":
            create_project()
        elif choice == "2":
            loaded_project = load_project()
            if loaded_project:
                print(f"Switching to main menu for project {loaded_project}...\n")
                subprocess.run(["python3", controller_path])
                sys.exit()
        elif choice == "3":
            list_projects()
        elif choice == "4":
            delete_project()
            print("Project deleted successfully.")
        elif choice == "5":
            print("Exiting.")
            sys.exit()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    start()