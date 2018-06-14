from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^request_code/$', request_code, name="request_code"),
    url(r'^submit/$', submit, name="submit"),
    url(r'^logout/$', logout, name="logout")
]