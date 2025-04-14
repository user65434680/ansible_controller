import json

def load_user_counts(path="user_counts.json"):
    with open(path, "r") as f:
        return json.load(f)

def extract_client_number(name):
    return int(name.replace("client", ""))

def client_ranking():
    try:
        num_needed = int(input("How many computers are needed? "))
    except ValueError:
        print("Please enter a valid number.")
        return
    
    try:
        user_counts = load_user_counts()
    except FileNotFoundError:
        print("Error: user_counts.json not found.")
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

    with open("ranked_clients.json", "w") as f:
        json.dump(ranked_data, f, indent=4)

    print("\nSaved selected clients to 'ranked_clients.json'.")

if __name__ == "__main__":
    client_ranking()
