#!/bin/bash

# Variables
host=localhost
pb_airflow=playbooks/airflow.yaml
pb_chartsgouv=playbooks/chartsgouv.yaml
pb_postgresql=playbooks/postgresql.yaml

# Ansible installation
echo "Installing Ansible on the control node ..."
python3 -m pip install --user ansible

# Function to deploy a playbook
deploy_playbook() {
    local pb="$1"
    echo "Deploying $pb ..."
    ansible-playbook -i "$host" "$pb"
}

# Menu
echo "Select the apps to deploy:"
echo "1) Airflow"
echo "2) PostgreSQL"
echo "3) Chartsgouv"
echo "4) All"
echo "5) Exit"

read -p "Enter your choice (1-5): " choice

echo "Début: $(date)"

case "$choice" in
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
        deploy_playbook "$pb_postgresql"
        deploy_playbook "$pb_airflow"
        deploy_playbook "$pb_chartsgouv"
        ;;
    5)
        echo "Exiting."
        exit 0
        ;;
    *)
        echo "Invalid option."
        exit 1
        ;;
esac

echo "Fin: $(date)"
