from ansible_utils import run_ansible_playbook
import os

c_path = os.path.dirname(os.path.abspath(__file__))

def assign_computers_manually(clients_file="clients.txt"):
    with open(clients_file, "r") as file:
        clients = [line.strip() for line in file if line.strip()]

    print("Select a client:")
    for i, client in enumerate(clients, start=1):
        print(f"{i}) {client}")

def assign_computers_automatically():
    run_ansible_playbook(f"{c_path}/echo_available_computers.yml")
    from clients_default.user_count import client_ranking
    client_ranking()