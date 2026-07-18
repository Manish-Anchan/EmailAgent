from composio import Composio
from app.config import settings

composio_client = Composio(api_key=settings.composio_api_key)

_gmail_auth_config_id = None


def get_gmail_auth_config_id() -> str:
    """
    Get or create a Composio-managed Gmail auth config.
    Cached after first call — only hits the API once.
    """
    global _gmail_auth_config_id

    if _gmail_auth_config_id:
        return _gmail_auth_config_id

    # Check if one already exists
    configs = composio_client.auth_configs.list(toolkit_slug="gmail")
    if configs.items:
        _gmail_auth_config_id = configs.items[0].id
        return _gmail_auth_config_id

    # Create one with Composio-managed OAuth
    config = composio_client.auth_configs.create(
        toolkit="gmail",
        options={
            "type": "use_composio_managed_auth",
            "name": "gmail-oauth",
        },
    )
    _gmail_auth_config_id = config.id
    return _gmail_auth_config_id