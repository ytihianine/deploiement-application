### Déployer la suite données


1) Dupliquer les fichiers de variables
``` bash
# cd deploiement-applications/ansible
cp roles/apps/airflow/vars/example.main.yaml roles/apps/airflow/vars/main.yaml
```

Par défaut,
- Installe Ansible sur la machine hôte
- Déploie Airflow

``` bash
# cd deploiement-applications/ansible
bash init.bash
```
