import json
import os

from django.conf import settings
from telethon import TelegramClient

from .models import TelegramAuthorization
from .exceptions import PayloadException, TelegramAuthorizationException


def parse_json_payload(body, *keys):
    try:
        raw_payload = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PayloadException("Cant decode body '%s'\n%s" % (body, exc))

    try:
        payload = json.loads(raw_payload)
    except (ValueError, TypeError) as exc:
        raise PayloadException("Can't load JSON from raw payload '%s'\n%s" % (raw_payload, exc))

    for key in keys:
        if key not in payload:
            raise PayloadException("Key '%s' was not found in payload '%s'" % (key, payload))

    return (payload.get(key) for key in keys)


def get_telegram_client(phone):
    client = TelegramClient(
        os.path.join(settings.DTA_TG_SESSION_DIR, "%s.telegram_session" % phone),
        settings.DTA_TG_API_ID,
        settings.DTA_TG_API_HASH,
        spawn_read_thread=False,
        report_errors=False
    )
    success = client.connect()
    if not success:
        raise TelegramAuthorizationException("Can't connect to telegram servers")

    return client


def telegram_is_logged_in(request):
    try:
        telegram_authorization = TelegramAuthorization.objects.get(user=request.user)
    except TelegramAuthorization.DoesNotExist:
        return False
    try:
        client = get_telegram_client(telegram_authorization.phone)
    except TelegramAuthorizationException as e:
        return False

    return client.is_user_authorized()
