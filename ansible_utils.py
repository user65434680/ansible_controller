import subprocess

def run_ansible_playbook(playbook, inventory="inventory/inventory.ini"):
    command = ['ansible-playbook', '-i', inventory, playbook, '--ask-become-pass']

    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
        print(f"Playbook {playbook} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running playbook {playbook}: {e.stderr}")

def add_to_inventory(username, ip_address, inventory_file="inventory.ini"):
    with open(inventory_file, 'a') as inventory:
        inventory.write(f"\n[clients]\n{username} ansible_host={ip_address} ansible_user={username}\n")