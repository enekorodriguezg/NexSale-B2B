from server.core.app_settings import app_settings
from server.schemas.settings_schema import SettingsResponse, SettingsUpdate

### --------------------------------------------------###

def get_settings() -> SettingsResponse:
    return SettingsResponse(
        company_name = app_settings.company_name,
        currency = app_settings.currency,
        low_stock_threshold = app_settings.low_stock_threshold
    )

def update_settings(settings_in: SettingsUpdate) -> SettingsResponse:
    app_settings.update(
        company_name = settings_in.company_name,
        currency = settings_in.currency,
        low_stock_threshold = settings_in.low_stock_threshold
    )
    return get_settings()