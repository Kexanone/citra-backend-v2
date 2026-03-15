from allauth.account import app_settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import import_attribute


def get_adapter(request=None) -> DefaultAccountAdapter:
    return import_attribute(app_settings.ADAPTER)(request)
