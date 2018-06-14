=====
Django Telethon Authorization
=====

Provide REST API for authorizing telegram sessions

Quick start
-----------

1. Add "django-telethon-authorization" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django-telethon-authorization',
    ]

2. Include django-telethon-authorization URL's in your project urls.py like this::

    path('telegram-auth/', include('django_telethon_authorization.urls')),

3. Run `python manage.py migrate` to create the  models.

Endpoints
------------

