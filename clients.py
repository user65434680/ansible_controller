import json

def load_user_counts(path="user_counts.json"):
    with open(path, "r") as f:
        return json.load(f)

def get_client_list(n):
    return [f"client{i}" for i in range(1, n + 1)]

def client_ranking():
    try:
        user_counts = load_user_counts()
    except FileNotFoundError:
        print("Error: user_counts.json not found.")
        return

    try:
        num_clients = int(input("How many clients are needed? "))
    except ValueError:
        print("Please enter a valid number.")
        return

    selected_clients = get_client_list(num_clients)

    valid_clients = [client for client in selected_clients if client in user_counts]

    if not valid_clients:
        print("No matching clients found in user_counts.json.")
        return

    sorted_clients = sorted(
        valid_clients,
        key=lambda c: (user_counts[c], int(c.replace("client", "")))
    )

    print("\nRanked Clients by Number of Users (Least to Most):")
    for client in sorted_clients:
        print(f"{client}: {user_counts[client]} users")

    ranked_data = {
        "ranked_clients": [
            {"name": client, "users": user_counts[client]}
            for client in sorted_clients
        ]
    }

    with open("ranked_clients.json", "w") as f:
        json.dump(ranked_data, f, indent=4)

    print("\nRanked client data saved to 'ranked_clients.json'.")

if __name__ == "__client_ranking__":
    client_ranking()
