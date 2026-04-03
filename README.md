# Déploiement d'applications

Ce projet est une suite de playbooks Ansible permettant de déployer des applications sur des clusters Kubernetes.

> Note: à date, le projet permet de déployerles applications uniquement en se trouvant sur le cluster Kubernetes de l'entreprise. (i.e impossible d'utiliser les API Kubernetes)

## Structure du projet

```
.
├── ansible/
│   ├── playbooks.yaml           # Configuration des playbooks
│   ├── ansible.cfg              # Configuration Ansible
│   ├── readme.md                # Documentation des playbooks
│   ├── playbooks/               # Répertoire des playbooks
│   └── roles/                   # Rôles Ansible
├── test/              # Dossier de tests du CLI
├── cli.py           # CLI principal
├── Makefile           # Fichier Makefile
├── README.md           # Documentation du projet
└── requirements.txt           # Dépendances Python
```

## Pré-requis

- Un cluster Kubernetes
- Un service VScode lancé dans le cluster Kubernetes

## Applications

Pour déployer les playbooks, merci d'utiliser cette [documentation](ansible/readme.md)

Les applications disponibles sont:
- Airflow
- CharsGouv (Apache Superset)
- Postgres
- n8n
- Apache Polaris
- Trino

## Installation de l'environnement

Pour installer toutes les dépendances python
```bash
# Python & Ansible
make install
# Uniquement Python
make install-packages
# Uniquement Ansible
make install-collections
```

## Déployer une application

Commencer par dupliquer les fichiers de variables:
```bash
make duplicate
```

La doc [ansible/readme.md](ansible/readme.md) fournit les commandes pour exécuter les playbooks
