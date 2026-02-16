## social_media_api (Django + DRF Token Authentication)
A Django REST API starter project for a social media-style user system featuring:
* Custom `User` model (extends `AbstractUser`)
* Token-based authentication (DRF TokenAuth)
* User registration & login (both return a token)
* Authenticated user profile endpoint
* Followers system (self-referencing ManyToMany)
* Profile picture upload support

---

# Requirements
* Python 3.x
* Django
* Django REST Framework

---

# Install dependencies:

```bash
pip install django djangorestframework djangorestframework-authtoken pillow
```

> `pillow` is required for Django `ImageField`.

---

# Create Project & App

```bash
django-admin startproject social_media_api
cd social_media_api
python manage.py startapp accounts
```

---

# Configure `settings.py`

Open: `social_media_api/settings.py`

# Add installed apps

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework.authtoken",

    # Local apps
    "accounts",
]
```

# Set custom user model

```python
AUTH_USER_MODEL = "accounts.User"
```

# DRF settings (Token Authentication)

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

# Media settings (for profile pictures)

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

---

# Custom User Model

File: `accounts/models.py`

The project uses a custom `User` model extending `AbstractUser` with:

* `bio` (TextField)
* `profile_picture` (ImageField)
* `followers` (ManyToMany to self, `symmetrical=False`, `related_name="following"`)

Relationship meaning:

* `user.followers.all()` → users who follow `user`
* `user.following.all()` → users that `user` follows

---

# Authentication (TokenAuth)

Token authentication is enabled by adding:

* `rest_framework.authtoken` to `INSTALLED_APPS`
* DRF Token Authentication class to `REST_FRAMEWORK`

Tokens are created/returned by the **register** and **login** endpoints.

---

## Accounts API Endpoints

Base path:

```
/api/accounts/
```

# Register

* **POST** `/api/accounts/register`
* Creates a user and returns a token

# Login

* **POST** `/api/accounts/login`
* Authenticates and returns a token

# Profile

* **GET** `/api/accounts/profile` (auth required)
* **PUT/PATCH** `/api/accounts/profile` (auth required)

## Auth Header Format

For protected routes, include:

```
Authorization: Token <your_token_here>
```

---

## URL Configuration

# `accounts/urls.py`

Routes:

* `/register`
* `/login`
* `/profile`

# `social_media_api/urls.py`

Includes accounts routes under:

```
/api/accounts/
```

Also serves media during development when `DEBUG=True`.

---

## Migrations & Run Server

Run migrations (after setting `AUTH_USER_MODEL`):

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

---

## Testing with Postman

# Register

**POST** `http://127.0.0.1:8000/api/accounts/register`

Body (JSON):

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "StrongPass123",
  "bio": "Hello!"
}
```

Response:

```json
{
  "token": "...",
  "user": { ... }
}
```

# Login

**POST** `http://127.0.0.1:8000/api/accounts/login`

```json
{
  "username": "alice",
  "password": "StrongPass123"
}
```

# Profile

**GET** `http://127.0.0.1:8000/api/accounts/profile`

Header:

```
Authorization: Token <your_token_here>
```

Example PATCH:

```json
{
  "bio": "Updated bio"
}
```

---

### Project Setup Files

* Django project configuration (`settings.py`, `urls.py`, etc.)
* Installed apps and DRF token auth configuration
* Media configuration for profile pictures

# Code Files (accounts app)

* `models.py` (custom user model)
* `serializers.py` (register/login/profile)
* `views.py` (register/login/profile endpoints)
* `urls.py` (routing)
* `admin.py` (admin registration)

# Migrations

* `accounts/migrations/0001_initial.py` generated after running migrations

---

## Suggested Project Structure

```
social_media_api/
  manage.py
  db.sqlite3
  social_media_api/
    __init__.py
    settings.py
    urls.py
    wsgi.py
    asgi.py
  accounts/
    __init__.py
    admin.py
    apps.py
    models.py
    serializers.py
    views.py
    urls.py
    migrations/
    __init__.py
    0001_initial.py
  README.md
```
