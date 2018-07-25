=====
Django Telethon Authorization
=====

Provide REST API for authorizing telethon sessions

Quick start
-----------

1. Add "django-telethon-authorization" to your INSTALLED_APPS setting::

    INSTALLED_APPS = [
        ...
        'django-telethon-authorization',
    ]

2. Include django-telethon-authorization URL's in your project urls.py like this::

    path('telegram-auth/', include('django_telethon_authorization.urls')),


3. Add environment variables::

* TG_API_ID = 111111
* TG_API_HASH = api_hash
* TG_SESSION_PATH = /path/to/sessions

Provide `TG_SESSION_PATH` only if you use SQLite as a session backend (Telethon default)

4. Run `python manage.py migrate` to create the  models.

Way of work
------------

- When you request a telegram code - `TelegramAuthorization` model will be created.
- It will be automatically linked to `request.user`

Endpoints
------------

All endpoints accept JSON payloads.::
Usually response has status code `200` with a JSON.::
Each response contains boolean `success` property which indicates if request was successfull.::
If `success` == `False` -> variable `message` will be present inside JSON response with explanation.::


* POST /request_code/
* payload: {phone: <phone>}
* POST /submit/
* payload: {phone: <phone>, code: <code>, password: <password>}
* POST /logout/
* payload: {phone: <phone>}