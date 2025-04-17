import os

DEFAULT_PROJECT_NUMBER = "0001"

current_project_number = None

def get_current_project_number():
    global current_project_number
    if current_project_number is None:
        print(f"Warning: 'current_project_number' is not set. Defaulting to '{DEFAULT_PROJECT_NUMBER}'.")
        current_project_number = DEFAULT_PROJECT_NUMBER
    return current_project_number

def set_current_project_number(project_number):
    global current_project_number
    if not project_number:
        print("Error: Project number cannot be empty.")
        return
    current_project_number = project_number
    print(f"Current project number set to: {current_project_number}")