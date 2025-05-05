#!/usr/bin/env python3

import subprocess
import os

def generate_ssh_key():
    """Generate an SSH key pair if it doesn't exist."""
    ssh_key_path = os.path.expanduser("~/.ssh/id_rsa")
    
    if not os.path.exists(ssh_key_path):
        print("SSH key not found. Generating one...")
        subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", ssh_key_path, "-N", ""], check=True)
    else:
        print("SSH key already exists.")

def copy_ssh_key_to_client():
    """Copy the SSH key to the client server using Ansible."""
    client_ip = input("Enter the client server IP address: ").strip()
    username = input("Enter the SSH username for the client server: ").strip()
    password = input("Enter the SSH password for the client server: ").strip()
    inventory_content = f"""
[clients]
{client_ip} ansible_user={username} ansible_ssh_pass={password} ansible_become_pass={password}
"""
    inventory_file = "temp_inventory.ini"
    with open(inventory_file, "w") as f:
        f.write(inventory_content)

    try:
        command = ['ansible-playbook', '-i', inventory_file, 'copy_ssh_keys.yml']
        subprocess.run(command, check=True)
        print(f"SSH key copied to {username}@{client_ip} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error copying SSH key: {e}")
    finally:
        if os.path.exists(inventory_file):
            os.remove(inventory_file)

if __name__ == "__main__":
    copy_ssh_key_to_client()