# Déployer les playbooks

Avant de déployer un playbook, il est nécessaire de dupliquer les fichiers de configurations avec la commande `make duplicate`.

## Apache Superset

Pré-requis:
- Apache Superset: v6+
- PostgreSQL: v16+

1. Créer la base de données

Depuis votre service postgresql, exécuter la commande `CREATE DATABASE superset_config;`.

2. Configurer les fichiers de configuration

Dans le dossier `ansible/roles/app/chartsgouv`, des fichiers sont disponibles pour être configurés. Notamment les fichiers `files/superset_config_override.py` et le fichier `vars/main.yaml`.

3. Exécuter le playbook
Depuis la racine du projet:  
Manuellement: `ansible-playbook -i localhost ansible/playbooks/chartsgouv.yaml`
Via le CLI: 


### Troubleshooting

- **`Erreur: psycopg2 ModuleNotFound`**  

Depuis la version 4.1.0, Superset n'embarque aucun driver de base de données. Il est nécessaire de les installer soit même.  
**option 1**: réaliser une image custom de superset et y installer ses packages (recommandé)  
**option 2**: installer les packages via le script bootstrapt  
Pour l'option 2, il faut modifier le fichier `/templates/values.yaml.jinja` et y ajouter:
```
bootstrapScript: |
  #!/bin/bash
  # Si vous êtes derrière un proxy
  export HTTP_PROXY="http://host:port"
  export HTTPS_PROXY="http://host:port"
  # Installation des packages
  apt-get update && apt-get install -y build-essential
  uv pip install psycopg2-binary &&\
  if [ ! -f ~/bootstrap ]; then echo "Running Superset with uid {{ .Values.runAsUser }}" > ~/bootstrap; fi

```


## Apache polaris

Pré-requis:
- Apache Polaris: v1.3.0-incubating
- PostgreSQL: v16+

1. Créer la base de données
Depuis votre service postgresql, exécuter la commande `CREATE DATABASE polaris_config;`.

2. Exécuter le playbook
Depuis la racine du projet:  
Manuellement: `ansible-playbook -i localhost ansible/playbooks/polaris.yaml`
Via le CLI: 

3. Initialiser le catalog
Exécuter le script suivant en le complétant de vos informations => [script-init-polaris-catalog](https://forge.dgfip.finances.rie.gouv.fr/sg/dsci/lt/traitement-des-donnees/-/tree/main/scripts/catalogs?ref_type=heads)

4. Supprimer le déploiement

Depuis votre namespace
```
helm delete polaris-release-name
```

Depuis votre base postgresql
```
DROP DATABASE polaris_config WITH(force);
```