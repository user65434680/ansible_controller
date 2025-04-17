import os
import json

number_file = os.path.join(os.path.dirname(__file__), "number.json")

def get_current_project_number():
    if os.path.exists(number_file):
        with open(number_file, "r") as f:
            data = json.load(f)
            return data.get("current_project_number")
    else:
        print("number.json not found.")
        return None

def set_current_project_number(project_number):
    if not project_number:
        raise ValueError("Project number cannot be empty.")
    
    with open(number_file, "w") as f:
        json.dump({"current_project_number": project_number}, f, indent=4)
    
    print(f"Current project number set to: {project_number}")

current_project_number = get_current_project_number()