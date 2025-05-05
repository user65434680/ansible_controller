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

def copy_ssh_key_to_client():
    """Copy the SSH key to the client server using Ansible."""
    yml_path = os.path.join(c_path, "copy_ssh_keys.yml")

    try:
        command = ['ansible-playbook', '-i', yml_path, '--ask-become-pass']
        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error copying SSH key: {e}")

if __name__ == "__main__":
    copy_ssh_key_to_client()