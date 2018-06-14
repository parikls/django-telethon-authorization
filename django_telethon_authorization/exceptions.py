from django.http import JsonResponse


class BaseException(Exception):
    def __init__(self, message):
        self.message = message

    def to_response(self):
        return JsonResponse({"success": False, "message": self.message})


class PayloadException(BaseException):
    pass


class TelegramAuthorizationException(BaseException):
    pass
