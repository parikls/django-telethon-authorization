import logging

from django.http import JsonResponse
from telethon.errors import RPCError

from .exceptions import PayloadException, TelegramAuthorizationException
from .helpers import Telegram, require_post, login_required, parse_json_payload
from .models import TelegramAuthorization

logger = logging.getLogger("django-telethon-authorization")


@login_required
@require_post
def request_code(request):
    """ Accept JSON {phone: +xxxxxxxxxxx} """
    try:
        phone, = parse_json_payload(request.body, "phone")
    except PayloadException as e:
        logger.warning(e)
        return e.to_response()

    auth, _ = TelegramAuthorization.objects.get_or_create(user=request.user, phone=phone)

    try:
        client = Telegram.get_client(phone)
    except TelegramAuthorizationException as e:
        return e.to_response()

    if client.is_user_authorized():
        return JsonResponse({"success": False, "message": "You are already authorized"})
    try:
        response = client.send_code_request(phone)
        # hash will be needed during code submission
        auth.phone_code_hash = response.phone_code_hash
        auth.save()
        client.disconnect()
        return JsonResponse({"success": True})

    except RPCError as e:
        return JsonResponse(
            {"success": False, "message": "Telegram exception occurred. %s. %s" % (e.code, e.message)})

    except Exception as e:
        logger.exception("TG REQUEST CODE. POST. Error occurred during telegram send code")
        return JsonResponse({"success": False, "message": "'Error occurred during code sending\n%s'" % e})


@login_required
@require_post
def submit(request):
    try:
        phone, code = parse_json_payload(request.body, "phone", "code")
    except PayloadException as e:
        logger.exception(e)
        return e.to_response()

    try:
        auth = TelegramAuthorization.objects.get(user=request.user, phone=phone)
    except TelegramAuthorization.DoesNotExist:
        return JsonResponse({"success": False, "message": "Phone '%s' is invalid'" % phone})

    client = Telegram.get_client(phone)

    try:
        client.sign_in(auth.phone, code, phone_code_hash=auth.phone_code_hash)
        client.disconnect()

        # do not store hash after successful login
        auth.phone_code_hash = None
        auth.save()

    except RPCError as e:
        return JsonResponse(
            {"success": False, "message": "Telegram exception occurred. %s. %s" % (e.code, e.message)})

    except Exception as e:
        logger.warning("TG Login. POST. Error occurred during telegram sign-in\n%s" % e)
        return JsonResponse({"success": False, "message": "'Error occurred during telegram sign-in\n%s'" % e})
    return JsonResponse({"success": True})


@login_required
@require_post
def logout(request):
    try:
        phone = parse_json_payload(request.body, "phone")
    except PayloadException as e:
        logger.warning(e)
        return e.to_response()

    try:
        telegram_authorization = TelegramAuthorization.objects.get(user=request.user, phone=phone)
    except TelegramAuthorization.DoesNotExist:
        return JsonResponse({"success": False, "message": "Phone '%s' is invalid'" % phone})

    client = Telegram.get_client(telegram_authorization.phone)

    if client.log_out():
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "message": "Telegram RPC error"})
