from custom_config.superset_feature_flags import SECRET_KEY, FEATURE_FLAGS
from custom_config.superset_talisman import TALISMAN_ENABLED, TALISMAN_CONFIG
from custom_config.superset_theme import (
    THEME_OVERRIDES,
    EXTRA_CATEGORICAL_COLOR_SCHEMES,
    EXTRA_SEQUENTIAL_COLOR_SCHEMES
)
from custom_config.superset_cache_config import (
    CACHE_DEFAULT_TIMEOUT,
    CACHE_CONFIG,
    DATA_CACHE_CONFIG,
    FILTER_STATE_CACHE_CONFIG,
    EXPLORE_FORM_DATA_CACHE_CONFIG,
)

# Default values
FAVICONS = [{"href": "/static/assets/dsfr/favicon/favicon.svg"}]
LOGO_TOOLTIP = "ChartsGouv"
APP_NAME = "ChartsGouv"

# Specify the App icon
APP_ICON = "/static/assets/local/images/app_icon.png"
