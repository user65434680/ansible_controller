#!/bin/bash

SCRIPT_PATH="/opt/ansible_icon/ansible_icon.py"
GENERAL_PATH="/opt/ansible_icon/start.sh"
SERVICE_PATH="/etc/systemd/system/ansible_icon.service"

if [[ "$EUID" -ne 0 ]]; then
  echo "Please run this script as root or with sudo."
  exit 1
fi


mkdir -p /opt/ansible_icon
sudo cp ansible_project_icon/ansible_icon.py "$SCRIPT_PATH"
sudo cp ansible_project_icon/start.sh "$GENERAL_PATH"


sudo chmod 755 /opt/ansible_icon
sudo chmod 755 "$SCRIPT_PATH"
sudo chmod 755 "$GENERAL_PATH"
sudo chown root:root "$SCRIPT_PATH"
sudo chown root:root "$GENERAL_PATH"


cat <<EOF > "$SERVICE_PATH"
[Unit]
Description=Network Scan Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $SCRIPT_PATH
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF


systemctl daemon-reload
systemctl enable ansible_icon.service
echo "Service enabled to run on boot: ansible_icon.service"