#! /bin/bash

cat ./airflow/values_template.yaml > ./airflow/values.yaml
cat ./chartsgouv/values_template.yaml > ./chartsgouv/values.yaml
cat ./redis/values_template.yaml > ./redis/values.yaml

echo "Values files have been duplicated. It's time to config them ! " 