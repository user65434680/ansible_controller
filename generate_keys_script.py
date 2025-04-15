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

def copy_ssh_key_to_client(client_ip, username):
    """Copy the SSH key to the client server's authorized_keys file."""
    ssh_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
    
    if not os.path.exists(ssh_key_path):
        generate_ssh_key()
    
    try:
        print(f"Copying SSH key to {username}@{client_ip}...")
        subprocess.run(["ssh-copy-id", "-i", ssh_key_path, f"{username}@{client_ip}"], check=True)
        print(f"SSH key copied to {username}@{client_ip} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error copying SSH key: {e}")

def generate_ssh_keys_for_clients():
    client_ip = input("Enter the client server IP address: ").strip()
    username = input("Enter the SSH username for the client server: ").strip()
    
    copy_ssh_key_to_client(client_ip, username)

if __name__ == "__main__":
    generate_ssh_keys_for_clients()