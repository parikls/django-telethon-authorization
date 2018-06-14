import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from telethon.errors import RPCError

from .exceptions import PayloadException, TelegramAuthorizationException
from .models import TelegramAuthorization
from .utils import parse_json_payload, get_telegram_client

logger = logging.getLogger("django-telethon-authorization")


@login_required
@require_POST
def request_code(request):
    """ Accept JSON {phone: +xxxxxxxxxxx} """
    try:
        phone, = parse_json_payload(request.body, "phone")
    except PayloadException as e:
        logger.warning(e)
        return e.to_response()

    auth, _ = TelegramAuthorization.objects.get_or_create(user=request.user, phone=phone)

    try:
        client = get_telegram_client(phone)
    except TelegramAuthorizationException as e:
        return e.to_response()

    if client.is_user_authorized():
        return JsonResponse({"success": False, "code": -1, "error": "You are already authorized"})
    try:
        response = client.send_code_request(phone)
        auth.phone_code_hash = response.phone_code_hash
        auth.save()
        client.disconnect()
        return JsonResponse({"success": True})

    except RPCError as e:
        return JsonResponse(
            {"success": False, "code": -1, "error": "Telegram exception occurred. %s. %s" % (e.code, e.message)})

    except Exception as e:
        logger.warning("TG REQUEST CODE. POST. Error occurred during telegram send code\n%s" % e)
        return JsonResponse({"success": False, "error": "'Error occurred during code sending\n%s'" % e})


@login_required
@require_POST
def submit(request):
    try:
        phone, code = parse_json_payload(request.body, "phone", "code")
    except PayloadException as e:
        logger.warning(e)
        return e.to_response()

    try:
        auth = TelegramAuthorization.objects.get(user=request.user, phone=phone)
    except TelegramAuthorization.DoesNotExist:
        return JsonResponse({"success": False, "error": "Phone '%s' is invalid'" % phone})

    client = get_telegram_client(phone)

    try:
        client.sign_in(auth.phone, code, phone_code_hash=auth.phone_code_hash)
        client.disconnect()

        # do not store code or hash after successful login
        auth.phone_code_hash = None
        auth.save()

    except RPCError as e:
        return JsonResponse(
            {"success": False, "code": -1, "error": "Telegram exception occurred. %s. %s" % (e.code, e.message)})

    except Exception as e:
        logger.warning("TG Login. POST. Error occurred during telegram sign-in\n%s" % e)
        return JsonResponse({"success": False, "error": "'Error occurred during telegram sign-in\n%s'" % e})
    return JsonResponse({"success": True})


@login_required
@require_POST
def logout(request):
    try:
        phone = parse_json_payload(request.body, "phone")
    except PayloadException as e:
        logger.warning(e)
        return e.to_response()

    try:
        telegram_authorization = TelegramAuthorization.objects.get(user=request.user, phone=phone)
    except TelegramAuthorization.DoesNotExist:
        return JsonResponse({"success": False, "error": "Phone '%s' is invalid'" % phone})

    client = get_telegram_client(telegram_authorization.phone)

    if client.log_out():
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "code": -1, "error": "Telegram RPC error"})
