#!/usr/bin/env python3

import os
import subprocess
import json

def allow_domains():
    domain_list = input("Please input domains in allowed format (youtube.com): ").strip()


    if os.path.exists('allowed_domains.json') and os.path.getsize('allowed_domains.json') > 0:
        try:
            with open('allowed_domains.json', 'r') as file:
                existing_domains = json.load(file)
        except json.JSONDecodeError:
            print("Invalid JSON format found in allowed_domains.json, starting fresh.")
            existing_domains = {"domains": []}
    else:
        existing_domains = {"domains": []}


    if domain_list and domain_list not in existing_domains["domains"]:
        existing_domains["domains"].append(domain_list)


        with open('allowed_domains.json', 'w') as file:
            json.dump(existing_domains, file, indent=4)

        print(f"Added domain: {domain_list}")
    else:
        print(f"Domain '{domain_list}' is already in the list or input was empty.")


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
