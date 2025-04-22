#!/usr/bin/env python3

from project_manager import ensure_projects_folder, list_projects, create_project, load_project
import subprocess
import os
import sys

def start():
    ensure_projects_folder()
    while True:
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
            loaded_project = load_project()
            if loaded_project:
                print(f"Switching to main menu for project {loaded_project}...\n")
                subprocess.run(["python3", "controller.py"])
                sys.exit()
        elif choice == "3":
            list_projects()
        elif choice == "4":
            print("Exiting.")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    start()