#!/bin/bash

# Basic requirements installation
sudo apt install python3 python3-pip -y
sudo apt-get install ansible -y
ansible-galaxy collection install ansible.posix
sudo apt install sshpass -y
sudo apt install libssl-dev python3-dev build-essential -y
sudo apt install python3-openssl -y

# Segment for optional scanning tools
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
fi

echo "Installation complete!"