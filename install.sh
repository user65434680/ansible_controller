#!/bin/bash

# Basic requirements installation
sudo apt install python3 python3-pip -y
sudo apt-get install ansible -y
ansible-galaxy collection install ansible.posix
sudo apt install sshpass -y
sudo apt install libssl-dev python3-dev build-essential -y
sudo apt install python3-openssl -y

sudo ../ansible_project_icon/setup_ansible_icon.sh

# Segment for optional scanning tools
echo "Would you like to install Suricata and network scanning tools?"
echo "This requires two network interfaces for the computer."
read -p " (y/n): " choice
if [[ "$choice" =~ ^[Yy]$ ]]; then

    git clone https://github.com/user65434680/network_scanner network_scanner
    cd network_scanner
    chmod +x run_all.sh
    sudo ./run_all.sh
    echo "[!!] MOVING DIRECTORY TO /opt/ansible_controller SCRIPT WILL TERMINATE[!!]"


    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    DEST="/path/to/where/you/want/to/move"

    mv "$SCRIPT_DIR" "$DEST"
else
    echo "Skipping Suricata and network scanning tools installation..."
    echo "[*] Scheduling system reboot in 10 seconds..."
    sudo shutdown -r +1 "System will reboot in 10 seconds"
    echo "[!!] MOVING DIRECTORY TO /opt/ansible_controller SCRIPT WILL TERMINATE[!!]"
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    DEST="/path/to/where/you/want/to/move"
    mv "$SCRIPT_DIR" "$DEST"
fi