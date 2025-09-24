#!/bin/bash

# Ansible installation
echo Installing Ansible on the control node ...
python3 -m pip install --user ansible

# App deployment
ansible-playbook -i localhost playbooks/airflow.yaml