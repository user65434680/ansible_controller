#!/usr/bin/env python3

import subprocess
import os

c_path = os.path.dirname(os.path.abspath(__file__))

def generate_ssh_key():
    """Generate an SSH key pair if it doesn't exist."""
    ssh_key_path = os.path.expanduser("~/.ssh/id_rsa")
    
    if not os.path.exists(ssh_key_path):
        print("SSH key not found. Generating one...")
        subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", ssh_key_path, "-N", ""], check=True)
    else:
        print("SSH key already exists.")

def copy_ssh_key_to_client(client_ip, username):
    """Copy the SSH key to the client server using Ansible."""
    yml_path = os.path.join(c_path, "copy_ssh_keys.yml")
    inventory_content = f"""
[clients]
{client_ip} ansible_user={username}
"""
    inventory_file = "temp_inventory.ini"
    with open(inventory_file, "w") as f:
        f.write(inventory_content)

    try:
        command = ['ansible-playbook', '-i', inventory_file, yml_path, '--ask-pass' '--ask-become-pass']
        subprocess.run(command, check=True)
        print(f"SSH key copied to {username}@{client_ip} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error copying SSH key: {e}")
    finally:
        if os.path.exists(inventory_file):
            os.remove(inventory_file)

if __name__ == "__main__":
    copy_ssh_key_to_client()