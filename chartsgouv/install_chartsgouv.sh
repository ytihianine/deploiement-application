kubectl delete configmap superset-tmp-custom-extra-config
kubectl create configmap superset-tmp-custom-extra-config \
    --from-file=custom_config/superset_cache_config.py \
    --from-file=custom_config/superset_custom_security_manager.py \
    --from-file=custom_config/superset_custom_user_model.py \
    --from-file=custom_config/superset_feature_flags.py \
    --from-file=custom_config/superset_html_sanitization.py \
    --from-file=custom_config/superset_jinja_context_addons.py \
    --from-file=custom_config/superset_talisman.py \
    --from-file=custom_config/superset_theme.py

helm repo add superset http://apache.github.io/superset/
helm repo update superset
helm upgrade --install chartsgouv-mef-sg superset/superset -f values.yaml \
    --set-file=configOverrides.config_override=superset_config_override.py
