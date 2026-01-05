#!/bin/bash

# Variables
host=localhost
pb_airflow=playbooks/airflow.yaml
pb_chartsgouv=playbooks/chartsgouv.yaml
pb_postgresql=playbooks/postgresql.yaml
pb_n8n=playbooks/n8n.yaml

# Ansible installation
echo "Installing Ansible on the control node ..."
python3 -m pip install --user ansible

# Function to duplicate
duplicate_files() {
    echo "Duplicating files ..."
    find . -type f -name "example.main.yaml" -exec sh -c '
        target="$(dirname "$1")/main.yaml"
        cp "$1" "$target"
        echo "Created: $target"
    ' _ {} \;
}

# Function to deploy a playbook
deploy_playbook() {
    local pb="$1"
    echo "Deploying $pb ..."
    ansible-playbook -i "$host" "$pb"
}

# Menu
echo "Select the apps to deploy:"
echo "0) Dupliquer fichiers d'exemple"
echo "1) Airflow"
echo "2) PostgreSQL"
echo "3) Chartsgouv"
echo "4) N8N"
echo "5) All"
echo "6) Exit"

read -p "Enter your choice (0-6): " choice

echo "Début: $(date)"

case "$choice" in
    0)
        duplicate_files
        ;;
    1)
        deploy_playbook "$pb_airflow"
        ;;
    2)
        deploy_playbook "$pb_postgresql"
        ;;
    3)
        deploy_playbook "$pb_chartsgouv"
        ;;
    4)
        deploy_playbook "$pb_n8n"
        ;;
    5)
        deploy_playbook "$pb_postgresql"
        deploy_playbook "$pb_airflow"
        deploy_playbook "$pb_chartsgouv"
        ;;
    6)
        echo "Exiting."
        exit 0
        ;;
    *)
        echo "Invalid option."
        exit 1
        ;;
esac

echo "Fin: $(date)"
