from project_manager import ensure_projects_folder, list_projects, create_project, load_project
from projects.project_context import get_current_project_number
import subprocess
import os

current_project_number = get_current_project_number()

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
            subprocess.run(["python3", "controller.py"])
    elif choice == "3":
        list_projects()
    elif choice == "4":
        print("Exiting.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    start()