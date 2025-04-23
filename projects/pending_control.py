import os
import json

def add_to_pending(projects_path, current_project_number, category, item):
    """
    Add an item to a specific category in the pending.json file.

    Args:
        projects_path (str): Path to the projects directory.
        current_project_number (str): The current project number.
        category (str): The category to update (e.g., "apparmor_changes").
        item (str): The item to add to the category.
    """
    pending_file = os.path.join(projects_path, current_project_number, "pending.json")

    if os.path.exists(pending_file):
        with open(pending_file, "r") as f:
            pending_data = json.load(f)
    else:
        pending_data = {
            "user_changes": [],
            "domain_changes": [],
            "apparmor_changes": []
        }

    if item not in pending_data.get(category, []):
        pending_data[category].append(item)

    with open(pending_file, "w") as f:
        json.dump(pending_data, f, indent=4)

    print(f"Added '{item}' to '{category}' in {pending_file}")