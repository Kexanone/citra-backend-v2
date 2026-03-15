from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'citra_account'

    def ready(self):
        import citra_account.signals  # noqa: F401
