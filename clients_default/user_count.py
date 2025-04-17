#!/usr/bin/env python3

import json
import os

c_path = os.path.dirname(os.path.abspath(__file__))
user_counts_file = os.path.join(c_path, "user_counts.json")
ranked_clients_file = os.path.join(c_path, "ranked_clients.json")

def load_user_counts(path=user_counts_file):
    with open(path, "r") as f:
        return json.load(f)

def client_ranking():
    try:
        num_needed = int(input("How many computers are needed? "))
    except ValueError:
        print("Please enter a valid number.")
        return
    
    try:
        user_counts = load_user_counts()
    except FileNotFoundError:
        print(f"Error: {user_counts_file} not found.")
        return

    all_clients = {k: v for k, v in user_counts.items() if k.startswith("client") and k[6:].isdigit()}

    sorted_clients = sorted(
        all_clients.items(),
        key=lambda item: (item[1], extract_client_number(item[0]))
    )

    chosen_clients = sorted_clients[:num_needed]

    print("\nSelected Clients:")
    for name, count in chosen_clients:
        print(f"{name}: {count} users")

    ranked_data = {
        "ranked_clients": [
            {"name": name, "users": count}
            for name, count in chosen_clients
        ]
    }

    with open(ranked_clients_file, "w") as f:
        json.dump(ranked_data, f, indent=4)

    print(f"\nSaved selected clients to '{ranked_clients_file}'.")

def extract_client_number(name):
    return int(name.replace("client", ""))

if __name__ == "__main__":
    client_ranking()
