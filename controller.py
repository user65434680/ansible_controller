import json
import random
import string

def load_user_data():
    try:
        with open('user_data.json', 'r') as file:
            return json.load(file)  # Load JSON data
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist

def save_user_data(data):
    with open('user_data.json', 'w') as file:
        json.dump(data, file, indent=4)  # Save data to JSON file with nice formatting

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + "!?"
    return ''.join(random.choice(characters) for _ in range(length))

def add_user():
    print("\n--- Adding Users ---")
    user_data = load_user_data()  # Load existing user data

    if 'users' not in user_data:
        user_data['users'] = []  # Ensure 'users' key exists

    while True:
        username = input("Enter username (or type 'exit' to stop): ").strip()
        if username.lower() == 'exit':
            break

        password_choice = input("Would you like to either\n1) Enter passwords manually\n2) Generate a random password automatically (8 characters)?\nChoose 1 or 2: ").strip()

        if password_choice == "1":
            password = input("Enter password: ").strip()
        elif password_choice == "2":
            password = generate_random_password()  # Generate a random password
        else:
            print("Invalid choice. Try again.")
            continue

        user_data['users'].append({
            'username': username,
            'password': password
        })

        print(f"User '{username}' has been added.")

    save_user_data(user_data)  # Save updated data back to the JSON file

    print("Users have been added to user_data.json.")

def main():
    print("Select an option:")
    print("1. Add user")
    print("2. Exit")

    choice = input("Enter the number of your choice: ").strip()

    if choice == "1":
        add_user()
    elif choice == "2":
        print("Exiting...")
    else:
        print("Invalid choice. Exiting.")

if __name__ == '__main__':
    main()
