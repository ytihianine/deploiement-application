# Déployer une instance Airflow
Ce guide est réalisé dans le cadre du [programme 10%](https://www.10pourcent.etalab.gouv.fr/).
L'objectif est de fournir les éléments essentiels pour déployer une instance Airflow dans un environnement Kubernetes.

## Configuration générale
Avant toute chose, dupliquer le fichier `values_template.yaml` et renommer le `values.yaml`.
Toutes les modifications suivantes seront à apporter dans le fichier `values.yaml`.

- __Airflow__
Il y a deux valeurs à configurer:
```
fernetKey: renseignez votre valeur
webserverSecretKey: renseignez votre valeur
```

- __Base de données__
Airflow stocke un ensemble d'éléments dans une base de données (les logs par exemple).
Ce guide utilisera une base PostgreSQL.

1) Créer un service de base de données
- Si vous avez déjà un service base de donnée de lancé, le mieux est de créer une database dédiée à votre instance Airflow avec la commande suivante:
`CREATE DATABASE airflow_demo`

- Si vous n'avez pas de service de base de données déjà lancé: depuis l'interface web de Nubonyxia, lancez un service PostgreSQL et créez la database associée avec la commande du point précédent.

Airflow ira créer toutes les tables dont il a besoin dans le schéma public de votre database.

2) Créer un secret
Les credentials pour accéder dans votre base de données doivent être stockées dans un secret.

```
kubectl create secret generic database-credentials \
  --from-literal=username='postgresql username' \
  --from-literal=password='postgresql password'
```

3) Configurer le fichier values.yaml
La partie suivante doit être configurée en fonction de vos paramètres:
```
postgresql:
  ## to use the external db, the embedded one must be disabled
  enabled: false

externalDatabase:
  type: postgres

  host: host de votre base de données (ex: postgresql-123456)
  port: 5432

  ## the schema which will contain the airflow tables
  database: airflow_demo

  ## Kubernetes secret in your airflow namespace
  userSecret: "database-credentials"
  userSecretKey: "username"
  passwordSecret: "database-credentials"
  passwordSecretKey: "password"
```

- __Host__
Il s'agit de l'url qui sera utilisée pour accéder à l'interface web d'Airflow.
L'host se configure dans le `ingress`.
```
# Exemple
ingress:
  enabled: true
  web:
    enabled: true
    ingressClassName: nginx
    host: "mon-instance-airflow.lab.incubateur.finances.rie.gouv.fr"
```

- __Synchroniser un repo git__
Pour créer des pipelines, vous aurez besoin d'associer un repos git à votre instance Airflow. La méthode recommandée est d'utilisée le Git-Sync en HTTP.
Deux étapes sont nécessaires pour synchroniser un repo git en HTTP avec votre instance Airflow.

1) Générer un token d'accès
Airflow a besoin d'avoir un token d'accès pour synchroniser ses pipelines. Par défaut, Airflow se synchronise toutes les 60 secondes.
GitHub : [documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)
GitLab : [documentation](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#create-a-personal-access-token)

Vous pouvez limiter les droits de votre token au repo en question et à la lecture seule.

2) Créer un secret dans votre namespace
Dans votre namespace, vous désormais créer votre secret qui contiendra les moyens d'accès à votre repo.
```
kubectl create secret generic le-nom-de-votre-secret \
  --from-literal=username='MY_GIT_USERNAME' \
  --from-literal=password='MY_GIT_TOKEN'
```

Il y a deux éléments à configurer:
```
dags:
  gitSync:
    repo: l'url de votre repo git - celle utilisée pour cloner le repo
    httpSecret: le nom du secret que vous venez de créer

    # Si vous modifier les clés de votre secret, il faut également modifier les lignes suivantes.
    httpSecretUsernameKey: username
    httpSecretPasswordKey: password
```

Si vous souhaitez utiliser une autre méthode, rendez-vous dans cette [section](https://github.com/airflow-helm/charts/blob/main/charts/airflow/docs/faq/dags/load-dag-definitions.md#option-1---git-sync-sidecar)


- __Installer le chart helm__
Pour installer le chart helm, exécutez les commandes suivantes en précisant le nom de votre instance:
```
helm repo add airflow-stable https://airflow-helm.github.io/charts
helm upgrade --install nom-instance-airflow airflow-stable/airflow -f ./values.yaml
```
Pour exécuter la 2ème commande, il est nécessaire de se placer dans le dossier où se situe votre fichier `values.yaml`.

## Pour plus d'informations
Vous trouverez plus d'informations de configuration sur ce [repo](https://github.com/airflow-helm/charts/tree/main/charts/airflow)
