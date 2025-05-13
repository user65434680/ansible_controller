#!/bin/bash

sudo apt install python3 python3-pip -y

sudo apt-get install ansible -y

ansible-galaxy collection install ansible.posix

sudo apt install libssl-dev python3-dev build-essential -y

sudo apt install python3-openssl -y