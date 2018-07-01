import os
from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured


class TelegramAuthConfig(AppConfig):
    name = 'django_telethon_authorization'

    def ready(self):
        if not (
            os.environ.get("TG_API_ID", None) and
            os.environ.get("TG_API_HASH", None)
        ):
            raise ImproperlyConfigured(
                "\nIn order to use django-telethon-authorization you must set environment variables:\n"
                "TG_API_ID\n"
                "TG_API_HASH"
            )
