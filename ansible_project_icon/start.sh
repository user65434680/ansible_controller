#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "This script must be run with sudo or as root."
  exit 1
fi

cd /opt/ansible_controller || {
  echo "Directory /opt/ansible_controller does not exist."
  exit 1
}
sudo python3 run.py
