#!/bin/bash

# Ansible installation
echo Installing Ansible on the control node ...
python3 -m pip install --user ansible

echo "Début: $(date)"
# App deployment
# ansible-playbook -i localhost playbooks/airflow.yaml
ansible-playbook -i localhost playbooks/postgresql.yaml

echo "Fin: $(date)"
