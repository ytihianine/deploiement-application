# Déployer les playbooks

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