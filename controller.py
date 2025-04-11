import subprocess
import sys

def run_ansible_playbook(playbook):
    try:
        result = subprocess.run(
            ['ansible-playbook', '-i', 'inventory.ini', playbook, '--ask-become-pass'],
            check=True, text=True, capture_output=True
        )
        print(result.stdout)
        print(f"Playbook {playbook} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running playbook {playbook}: {e.stderr}")
        
def create_user():
    run_ansible_playbook('users.yml')

def delete_user():
    run_ansible_playbook('del_users.yml')

def main():
    print("Select an option:")
    print("1. Create user")
    print("2. Delete user")

    choice = input("Enter the number of your choice: ").strip()

    if choice == "1":
        create_user()
    elif choice == "2":
        delete_user()
    else:
        print("Invalid choice. Exiting.")

if __name__ == '__main__':
    main()
