#!/usr/bin/env python3

import os
import subprocess
import json

def allow_domains():
    domain_list = input("Please input domains in allowed format (youtube.com): ").strip()

    if os.path.exists('allowed_domains.json'):
        with open('allowed_domains.json', 'r') as file:
            existing_domains = json.load(file)
    else:
        existing_domains = []

    if domain_list not in existing_domains:
        existing_domains.append(domain_list)

    with open('allowed_domains.json', 'w') as file:
        json.dump(existing_domains, file, indent=4)

    allow_domains_run()

def clear_allowed_domains():

    with open('allowed_domains.json', 'w') as file:
        json.dump([], file, indent=4)
    
    run_ansible_playbook_control('unbound_clear_domains.yml')

def clear_all():

    with open('allowed_domains.json', 'w') as file:
        json.dump([], file, indent=4)
    
    run_ansible_playbook_control('unbound_clear_blacklist.yml')

def allow_domains_run():
    run_ansible_playbook_control('unbound_whitelist.yml')

def run_ansible_playbook_control(playbook, ask_become_pass=False):
    command = ['ansible-playbook', '-i', 'inventory.ini', playbook, '--ask-become-pass']
    
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
        print(f"Playbook {playbook} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running playbook {playbook}: {e.stderr}")

def choose_action():
    while True:
        print("Select an option:")
        print("1. Allow domains")
        print("2. Clear allowed domains")
        print("3. Clear all domains and blacklist")
        print("4. Exit")

        choice = input("Enter the number of your choice: ").strip()

        if choice == "1":
            allow_domains()
        elif choice == "2":
            clear_allowed_domains()
        elif choice == "3":
            clear_all()
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    choose_action()
