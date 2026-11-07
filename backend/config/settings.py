
"""Django settings for Dental Clinic Backend."""

import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured
from django.utils.crypto import get_random_string

BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env (Render uses Environment Variables)
load_dotenv(BASE_DIR / ".env")


# --------------------------------------------------
# Environment helpers
# --------------------------------------------------

def env_bool(name, default=False):
    return os.getenv(
        name, "1" if default else "0"
    ).strip().lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    return [
        item.strip()
        for item in os.getenv(name, default).split(",")
        if item.strip()
    ]


# --------------------------------------------------
# Security
# --------------------------------------------------

DEBUG = env_bool("DJANGO_DEBUG", False)

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "")

if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY must be set when DJANGO_DEBUG is off."
        )
    SECRET_KEY = get_random_string(64)


ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1"
)


# --------------------------------------------------
# Applications
# --------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",

    "apps.accounts",
    "apps.hero_images",
    "apps.case_studies",
    "apps.website_settings",
    "apps.media_manager",
    "apps.dashboard",
]


# --------------------------------------------------
# Middleware
# --------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# --------------------------------------------------
# URLs / Templates
# --------------------------------------------------

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# --------------------------------------------------
# Database - Supabase PostgreSQL
# --------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "postgres"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
        "OPTIONS": {
            "sslmode": "require",
        },
        "CONN_MAX_AGE": 60,
    }
}


# --------------------------------------------------
# CORS / CSRF - Vercel Frontend
# --------------------------------------------------

CORS_ALLOWED_ORIGINS = env_list(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173"
)

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost:5173"
)

CORS_ALLOW_CREDENTIALS = True


# --------------------------------------------------
# Password Validation
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 10},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]


# --------------------------------------------------
# Language / Time
# --------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# --------------------------------------------------
# Static Files
# --------------------------------------------------

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# --------------------------------------------------
# Media Files
# --------------------------------------------------

MEDIA_URL = "/media/"

# Render filesystem is temporary.
# Use Supabase Storage for permanent uploaded images.
MEDIA_ROOT = Path(
    os.getenv("MEDIA_ROOT", str(BASE_DIR / "media"))
).resolve()


# --------------------------------------------------
# Default Model Field
# --------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --------------------------------------------------
# Django REST Framework
# --------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],

    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],

    "DEFAULT_THROTTLE_RATES": {
        "login": "5/min",
        "refresh": "30/min",
        "public": "300/min",
    },

    "EXCEPTION_HANDLER": "apps.common.exceptions.api_exception_handler",
}


# --------------------------------------------------
# JWT Authentication
# --------------------------------------------------

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),

    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "UPDATE_LAST_LOGIN": True,
}


REFRESH_COOKIE_NAME = "clinic_refresh"

REFRESH_COOKIE_PATH = "/api/auth/"


# --------------------------------------------------
# Cookies / Security
# --------------------------------------------------

SECURE_COOKIES = env_bool(
    "SECURE_COOKIES",
    not DEBUG
)

SESSION_COOKIE_SECURE = SECURE_COOKIES

CSRF_COOKIE_SECURE = SECURE_COOKIES

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SECURE_REFERRER_POLICY = "same-origin"


# --------------------------------------------------
# Business Limits
# --------------------------------------------------

HERO_MAX_IMAGES = int(
    os.getenv("HERO_MAX_IMAGES", "6")
)

MAX_IMAGE_BYTES = 15 * 1024 * 1024

MAX_LOGO_BYTES = 5 * 1024 * 1024

MAX_VIDEO_BYTES = 100 * 1024 * 1024


# --------------------------------------------------
# Logging
# --------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },

    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}
