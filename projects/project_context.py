#!/usr/bin/env python3

import os
import json

number_file = os.path.join(os.path.dirname(__file__), "project_number.json")

def get_current_project_number():
    """Retrieve the current project number from project_number.json."""
    if os.path.exists(number_file):
        with open(number_file, "r") as f:
            data = json.load(f)
            return data.get("current_project_number")
    else:
        print("Error: project_number.json not found.")
        return None