from django.http import JsonResponse


class DTAException(Exception):
    """ Base exception which could represent itself as a JSON response"""
    def __init__(self, message):
        self.message = message

    def to_response(self):
        return JsonResponse({"success": False, "message": self.message})


class PayloadException(DTAException):
    pass


class TelegramAuthorizationException(DTAException):
    pass
