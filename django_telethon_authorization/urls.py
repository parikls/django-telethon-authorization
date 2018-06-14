from django.conf.urls import url
from django.conf import settings
from .views import *

ALL_VIEWS = {
    "submit": submit,
    "request_code": request_code,
    "logout": logout
}

for name, view in ALL_VIEWS.items():
    if getattr(settings, "DTA_VIEWS_LOGIN_REQUIRED", False):
        ALL_VIEWS[name] = login_required(view)


urlpatterns = [
    url(r'^submit/$', ALL_VIEWS["submit"], name="submit"),
    url(r'^request_code/$', ALL_VIEWS["request_code"], name="request_code"),
    url(r'^logout/$', ALL_VIEWS["logout"], name="logout")
]