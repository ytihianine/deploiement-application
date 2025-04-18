kubectl create configmap superset-tmp-custom-extra-config \
    --from-file=superset_cache_config.py \
    --from-file=superset_custom_security_manager.py \
    --from-file=superset_custom_user_model.py \
    --from-file=superset_feature_flags.py \
    --from-file=superset_html_sanitization.py \
    --from-file=superset_jinja_context_addons.py \
    --from-file=superset_talisman.py \
    --from-file=superset_theme.py

helm repo add superset http://apache.github.io/superset/
helm repo update superset
helm upgrade --install your-instance-name superset/superset -f values.yaml \
    --set-file=configOverrides.config_override=superset_config_override.py
