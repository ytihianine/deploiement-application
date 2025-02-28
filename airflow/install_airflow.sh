helm repo add airflow-stable https://airflow-helm.github.io/charts
helm repo update
helm upgrade --install airflow-mef-sg airflow-stable/airflow -f ./values.yaml
