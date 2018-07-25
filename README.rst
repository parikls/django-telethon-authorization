=====
Django Telethon Authorization
=====

Provide REST API for authorizing telethon sessions

Quick start
-----------

1. Add "django-telethon-authorization" to your INSTALLED_APPS setting::

..code:: python
    INSTALLED_APPS = [
        ...
        'django-telethon-authorization',
    ]

2. Include django-telethon-authorization URL's in your project urls.py like this::
..code:: python
    path('telegram-auth/', include('django_telethon_authorization.urls')),


3. Add environment variables::

- TG_API_ID = 111111
- TG_API_HASH = api_hash
if you use SQLite as a session backend - also provide path to session directory::
- TG_SESSION_PATH = /path/to/sessions

4. Run `python manage.py migrate` to create the  models.

Way of work
------------

- When you request a telegram code - `TelegramAuthorization` model will be created.
- It will be automatically linked to `request.user`

Endpoints
------------

::
All endpoints accept JSON payloads.
Usually response has status code `200` with a JSON.
Each response contains boolean `success` property which indicates if request was successfull.
If `success` == `False` -> variable `message` will be present inside JSON response with explanation.


-endpoint: /request_code/
-type: POST
-payload: {phone: <phone>}

-endpoint: /submit/
-type: POST
-payload: {phone: <phone>, code: <code>, password: <password>}

-endpoint: /logout/
-type: POST
-payload: {phone: <phone>}