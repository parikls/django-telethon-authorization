from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class TelegramAuthConfig(AppConfig):
    name = 'django_telethon_authorization'

    def ready(self):
        if not (
            getattr(settings, "DTA_TG_SESSION_DIR", None) and
            getattr(settings, "DTA_TG_API_ID", None) and
            getattr(settings, "DTA_TG_API_HASH", None)
        ):
            raise ImproperlyConfigured(
                "\nIn order to use django-telethon-authorization you must set settings variables:\n"
                "DTA_TG_SESSION_DIR\n"
                "DTA_TG_API_ID\n"
                "DTA_TG_API_HASH"
            )
