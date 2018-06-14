=====
Django Telethon Authorization
=====

Provide REST API for authorizing telegram sessions

Quick start
-----------

1. Add "django-telethon-authorization" to your INSTALLED_APPS setting::

    INSTALLED_APPS = [
        ...
        'django-telethon-authorization',
    ]

2. Include django-telethon-authorization URL's in your project urls.py like this::

    path('telegram-auth/', include('django_telethon_authorization.urls')),


3. Add settings variables::

DTA_TG_SESSION_DIR = os.path.join(BASE_DIR, os.pardir, "telegram_sessions")
DTA_TG_API_ID = 111111
DTA_TG_API_HASH = "tg_api_hash"

4. Run `python manage.py migrate` to create the  models.

Way of work
------------

When you request a telegram code - `TelegramAuthorization` model will be created.
It will be automatically linked to `request.user`

Endpoints
------------

All endpoints accept JSON payloads. Usually response has status code `200` with
JSON in it's body with flag `success`, which indicates if request was successfull.
If `success` == `False` -> variable `message` will be present inside JSON response with explanation.

endpoint: /request_code/
type: POST
payload: {phone: <phone>}

endpoint: /submit/
type: POST
payload: {phone: <phone>, code: <code>}

endpoint: /logout/
type: POST
payload: {phone: <phone>}