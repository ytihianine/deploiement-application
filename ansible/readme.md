### Déployer la suite données

Ce mode de déploiement vise à répondre à plusieurs objectifs:
- Déployer la Suite Données de façon fiable, reproductible et rapide
- Mettre à jour les applications de façon modulaire

1) Dupliquer les fichiers de variables
``` bash
# cd deploiement-applications/ansible
cp roles/apps/airflow/vars/example.main.yaml roles/apps/airflow/vars/main.yaml
```
Seuls les fichiers `vars/main.yaml` sont exploités par Ansible pour la configuration des variables.

2) Déployer les applications

Pour déployer les applications, un script est mis à disposition et peut être exécuté avec la commande suivante:

``` bash
# cd deploiement-applications/ansible
bash init.bash
```

Ce script permet de déployer partiellement ou totalement l'ensemble des applicatifs liés à la **Suite Données**