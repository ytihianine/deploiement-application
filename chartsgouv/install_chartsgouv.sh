kubectl delete configmap superset-tmp-custom-extra-config
kubectl create configmap superset-tmp-custom-extra-config \
    --from-file=custom_config/cache_config.py \
    --from-file=custom_config/security_manager.py \
    --from-file=custom_config/user_model.py \
    --from-file=custom_config/feature_flags.py \
    --from-file=custom_config/html_sanitization.py \
    --from-file=custom_config/jinja_context_addons.py \
    --from-file=custom_config/talisman.py \
    --from-file=custom_config/theme.py

helm repo add superset http://apache.github.io/superset/
helm repo update superset
helm upgrade --install chartsgouv-mef-sg superset/superset -f values.yaml \
    --set-file=configOverrides.config_override=superset_config_override.py
