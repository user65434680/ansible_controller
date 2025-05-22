#!/bin/bash

sudo apt install python3 python3-pip -y
sudo apt-get install ansible -y
ansible-galaxy collection install ansible.posix
sudo apt install sshpass -y
sudo apt install libssl-dev python3-dev build-essential -y
sudo apt install python3-openssl -y

sudo ../ansible_project_icon/setup_ansible_icon.sh

echo "Would you like to install Suricata and network scanning tools?"
echo "This requires two network interfaces for the computer."
read -p " (y/n): " choice

if [[ "$choice" =~ ^[Yy]$ ]]; then
    git clone https://github.com/user65434680/network_scanner network_scanner
    cd network_scanner
    chmod +x run_all.sh
    sudo ./run_all.sh
else
    echo "Skipping Suricata and network scanning tools installation..."
    echo "[*] Scheduling system reboot in 10 seconds..."
    sudo shutdown -r +1 "System will reboot in 10 seconds"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="/opt/ansible_controller"

echo "[!!] Copying script to $DEST... [!!]"
sudo mkdir -p "$DEST"
sudo cp -r "$SCRIPT_DIR"/* "$DEST"

if [[ -f "$DEST/$(basename "$0")" ]]; then
    echo "Copy successful. Cleaning up source directory..."
    sudo rm -rf "$SCRIPT_DIR"
else
    echo "Copy failed. Skipping deletion of original directory."
fi
