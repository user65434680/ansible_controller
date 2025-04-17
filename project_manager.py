import os
import json
import random
from projects.project_context import get_current_project_number as project_id
import projects.project_context


PROJECTS_DIR = "projects"
ASSOCIATIONS_FILE = os.path.join(PROJECTS_DIR, "associations.json")

def ensure_projects_folder():
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)
        print("Created 'projects' folder.")
    else:
        print("'projects' folder already exists.")

def load_associations():
    if not os.path.exists(ASSOCIATIONS_FILE):
        return {}
    with open(ASSOCIATIONS_FILE, "r") as f:
        return json.load(f)

def save_associations(associations):
    with open(ASSOCIATIONS_FILE, "w") as f:
        json.dump(associations, f, indent=4)

def generate_unique_project_number():
    existing_numbers = {
        folder for folder in os.listdir(PROJECTS_DIR)
        if os.path.isdir(os.path.join(PROJECTS_DIR, folder)) and folder.isdigit()
    }

    while True:
        number = f"{random.randint(0, 9999):04}"
        if number != "0001" and number not in existing_numbers:
            return number

def create_project():
    project_name = input("Enter project name: ").strip()
    project_number = generate_unique_project_number()

    project_path = os.path.join(PROJECTS_DIR, project_number)
    os.makedirs(project_path)

    associations = load_associations()
    associations[project_number] = project_name
    save_associations(associations)

    print(f"Project '{project_name}' created with ID {project_number}.")

def load_project():
    project_name = input("Enter the project name to load: ").strip()
    associations = load_associations()

    for number, name in associations.items():
        if name.lower() == project_name.lower():
            projects.project_context.get_current_project_number = number
            print(f"Loaded project '{name}' with ID {number}.")
            return number

    print(f"Project '{project_name}' not found.")
    return None

def list_projects():
    associations = load_associations()
    if not associations:
        print("No projects found.")
        return

    print("\nProjects:")
    for name in associations.values():
        print(f"- {name}")