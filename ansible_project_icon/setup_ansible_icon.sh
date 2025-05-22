#!/bin/bash

# setup network scanner for controller
SCRIPT_PATH="/opt/ansible_icon/ansible_icon.py"
GENERAL_PATH="/opt/ansible_icon/RunAnsible.desktop"
SERVICE_PATH="/etc/systemd/system/ansible_icon.service"

if [[ "$EUID" -ne 0 ]]; then
  echo "Please run this script as root or with sudo."
  exit 1
fi
mkdir -p /opt/ansible_icon
sudo cp ansible_icon.py "$SCRIPT_PATH"
sudo cp RunAnsible.desktop "$GENERAL_PATH"

if [[ -f "$SCRIPT_PATH" ]]; then
  chmod +x "$SCRIPT_PATH"
  echo "Made $SCRIPT_PATH executable."
else
  echo "Error: Script $SCRIPT_PATH does not exist."
  exit 1
fi

cat <<EOF > "$SERVICE_PATH"
[Unit]
Description=Network Scan Service
After=network-online.target
Wants=network-online.target
RequiresMountsFor=/opt/ansible_icon

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/ansible_icon/ansible_icon.py
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

echo "Created systemd service file at $SERVICE_PATH."


systemctl daemon-reexec
systemctl daemon-reload
systemctl enable ansible_icon.service"

echo "Service enabled to run on boot: ansible_icon.service""

echo "Setting permissions..."
sudo chmod 700 /opt/ansible_icon
sudo chmod 700 /opt/ansible_controller/ansible_icon.py
sudo chown root:root /opt/ansible_controller/ansible_icon.py
sudo chmod +x /opt/ansible_icon/RunAnsible.desktop
