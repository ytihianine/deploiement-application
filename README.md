# Déploiement d'applications

Ce projet est une suite de playbooks Ansible permettant de déployer des applications sur des clusters Kubernetes.

> Note: à date, le projet permet de déployerles applications uniquement en se trouvant sur le cluster Kubernetes de l'entreprise. (i.e impossible d'utiliser les API Kubernetes)

## Structure du projet

```
.
├── ansible/
│   ├── playbooks.yaml           # Configuration des playbooks
│   ├── ansible.cfg              # Configuration Ansible
│   ├── readme.md              # Documentation des playbooks
│   ├── playbooks/               # Répertoire des playbooks
│   │   ├── airflow.yaml
│   │   ├── chartsgouv.yaml
│   │   ├── n8n.yaml
│   │   ├── postgresql-service.yaml
│   │   ├── postgresql-users.yaml
│   │   ├── postgresql-restore.yaml
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

Les applications disponibles sont:
- Airflow
- CharsGouv (Apache Superset)
- Postgres
- n8n

## Installation

Pour installer toutes les dépendances python
```bash
# Python & Ansible
make install
# Uniquement Python
make install-packages
# Uniquement Ansible
make install-collections
```

# CLI Ansible - Guide d'utilisation

Un outil en ligne de commande moderne et puissant pour gérer vos playbooks Ansible avec support de l'exécution parallèle et découverte automatique.

## 📖 Utilisation

### Lister les playbooks disponibles

```bash
./ansible_cli.py list
```

Avec détails complets :
```bash
./ansible_cli.py list -v
```

### Dupliquer les fichiers d'exemple

Copie automatiquement tous les fichiers `example.main.yaml` vers `main.yaml` :
```bash
./ansible_cli.py duplicate
```

### Exécuter un playbook

Un seul playbook :
```bash
./ansible_cli.py run postgresql-service
```

Plusieurs playbooks (séquentiel) :
```bash
./ansible_cli.py run postgresql-service airflow chartsgouv
```

### Exécution parallèle

Lancer plusieurs playbooks en parallèle :
```bash
./ansible_cli.py run airflow n8n chartsgouv --parallel
```

Avec contrôle du nombre de workers :
```bash
./ansible_cli.py run airflow n8n --parallel --max-workers 2
```

### Exécuter tous les playbooks

Tous les playbooks en séquentiel :
```bash
./ansible_cli.py run --all
```

Tous en parallèle :
```bash
./ansible_cli.py run --all --parallel
```

### Options avancées

#### Mode dry-run (simulation)
```bash
./ansible_cli.py run airflow --dry-run
```

#### Avec inventaire personnalisé
```bash
./ansible_cli.py run airflow -i inventory/production.ini
```

#### Variables supplémentaires
```bash
./ansible_cli.py run airflow --extra-vars '{"version": "2.5.0", "replicas": 3}'
```

#### Tags Ansible
Exécuter uniquement certains tags :
```bash
./ansible_cli.py run airflow --tags "install,configure"
```

Ignorer certains tags :
```bash
./ansible_cli.py run airflow --skip-tags "backup"
```

#### Verbosité
```bash
# Niveau 1
./ansible_cli.py run airflow -v

# Niveau 2
./ansible_cli.py run airflow -vv

# Niveau 3
./ansible_cli.py run airflow -vvv
```

#### Afficher la sortie complète
```bash
./ansible_cli.py run airflow --show-output
```

## 📝 Configuration

Le fichier `playbooks.yaml` permet de configurer les métadonnées de chaque playbook :

```yaml
playbooks:
  postgresql-service:
    description: "Déploie le service PostgreSQL sur Kubernetes"
    order: 1                    # Ordre d'exécution
    tags:
      - database
      - infrastructure
    requires: []                # Dépendances

  airflow:
    description: "Déploie Apache Airflow"
    order: 10
    tags:
      - application
    requires:
      - postgresql-service      # Sera exécuté après postgresql-service
```

### Propriétés disponibles

- **description** : Description du playbook
- **order** : Ordre d'exécution (nombre, plus petit = prioritaire)
- **tags** : Tags pour catégoriser les playbooks
- **requires** : Liste des playbooks prérequis (dépendances)

## 🎯 Exemples d'usage

### Déploiement complet de la Suite Données

```bash
# 1. Dupliquer les fichiers de configuration
./ansible_cli.py duplicate

# 2. Déployer toute l'infrastructure
./ansible_cli.py run --all --parallel
```

### Déploiement PostgreSQL avec utilisateurs

```bash
# Les dépendances sont résolues automatiquement
./ansible_cli.py run postgresql-users

# Équivalent à :
# 1. postgresql-service
# 2. postgresql-users
```

### Mise à jour d'une application spécifique

```bash
# Dry-run pour vérifier
./ansible_cli.py run airflow --dry-run -v

# Exécution réelle
./ansible_cli.py run airflow
```

### Déploiement de plusieurs applications en parallèle

```bash
./ansible_cli.py run airflow chartsgouv n8n --parallel --max-workers 3
```


## Ajouter un nouveau playbook

1. Créez votre playbook dans `playbooks/new-app.yaml`
2. (Optionnel) Ajoutez ses métadonnées dans `playbooks.yaml` :
   ```yaml
   playbooks:
     new-app:
       description: "Description de la nouvelle app"
       order: 15
       requires:
         - postgresql-service
   ```
3. Il sera automatiquement détecté :
   ```bash
   ./ansible_cli.py list
   ./ansible_cli.py run new-app
   ```

## 📄 License

Ce projet fait partie de la suite de déploiement d'applications.
