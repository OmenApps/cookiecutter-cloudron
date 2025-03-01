"""Django settings for {{ cookiecutter.project_slug }} project."""
from pathlib import Path

import environ
from csp.constants import SELF

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path("/app/data")  # Writable data directory

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
    DJANGO_ALLOWED_HOSTS=(list, ["*"]),
    DJANGO_CSRF_TRUSTED_ORIGINS=(list, ["https://{{ cookiecutter.location }}", "http://localhost"]),
    DJANGO_SECURE_SSL_REDIRECT=(bool, True),
    DJANGO_SECURE_HSTS_SECONDS=(int, 2592000),  # 30 days
    DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=(bool, True),
    DJANGO_SECURE_HSTS_PRELOAD=(bool, True),
    DJANGO_SESSION_COOKIE_SECURE=(bool, True),
    DJANGO_CSRF_COOKIE_SECURE=(bool, True),
)

# Take environment variables from .env file if it exists
environ.Env.read_env(BASE_DIR / ".env")

# Cloudron environment variables
CLOUDRON_APP_DOMAIN = env("CLOUDRON_APP_DOMAIN", default="localhost")
CLOUDRON_APP_ORIGIN = env("CLOUDRON_APP_ORIGIN", default="http://localhost")
CLOUDRON_MAIL_FROM = env("CLOUDRON_MAIL_FROM", default="noreply@localhost")
CLOUDRON_MAIL_SMTP_SERVER = env("CLOUDRON_MAIL_SMTP_SERVER", default="localhost")
CLOUDRON_MAIL_SMTP_PORT = env("CLOUDRON_MAIL_SMTP_PORT", default="25")
CLOUDRON_MAIL_SMTP_USERNAME = env("CLOUDRON_MAIL_SMTP_USERNAME", default="")
CLOUDRON_MAIL_SMTP_PASSWORD = env("CLOUDRON_MAIL_SMTP_PASSWORD", default="")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY", default="django-insecure-change-this-in-production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env("DJANGO_CSRF_TRUSTED_ORIGINS")

# Ensure the correct header is set for HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.socialaccount",
    {% if cookiecutter.use_cloudron_auth == "yes" %}
    "allauth.socialaccount.providers.openid_connect",
    {% endif %}
    "corsheaders",
    "crispy_forms",
    "crispy_bootstrap5",
    "debug_toolbar",
    "django_extensions",
    "django_htmx",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "ninja",
    "template_partials",
    {% if cookiecutter.use_scheduler == "yes" %}
    "django_celery_beat",
    {% endif %}
]

LOCAL_APPS = [
    "{{ cookiecutter.project_slug }}.common.apps.CommonConfig",
    "{{ cookiecutter.project_slug }}.users.apps.UsersConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "{{ cookiecutter.project_slug }}.common.middleware.LogRequestsMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "csp.middleware.CSPMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "{{ cookiecutter.project_slug }}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": ["template_partials.templatetags.partials"],
        },
    },
]

WSGI_APPLICATION = "{{ cookiecutter.project_slug }}.wsgi.application"
ASGI_APPLICATION = "{{ cookiecutter.project_slug }}.asgi.application"

# Database
{% if cookiecutter.database == "postgresql" %}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("CLOUDRON_POSTGRESQL_DATABASE"),
        "USER": env("CLOUDRON_POSTGRESQL_USERNAME"),
        "PASSWORD": env("CLOUDRON_POSTGRESQL_PASSWORD"),
        "HOST": env("CLOUDRON_POSTGRESQL_HOST"),
        "PORT": env("CLOUDRON_POSTGRESQL_PORT"),
        "CONN_MAX_AGE": env.int("CONN_MAX_AGE", default=60),
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}
{% else %}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("CLOUDRON_MYSQL_DATABASE"),
        "USER": env("CLOUDRON_MYSQL_USERNAME"),
        "PASSWORD": env("CLOUDRON_MYSQL_PASSWORD"),
        "HOST": env("CLOUDRON_MYSQL_HOST"),
        "PORT": env("CLOUDRON_MYSQL_PORT"),
        "CONN_MAX_AGE": env.int("CONN_MAX_AGE", default=60),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
            "connect_timeout": 10,
        }
    }
}
{% endif %}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cache
{% if cookiecutter.use_redis == "yes" %}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://:{env('CLOUDRON_REDIS_PASSWORD')}@{env('CLOUDRON_REDIS_HOST')}:{env('CLOUDRON_REDIS_PORT')}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    }
}
{% endif %}

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = CLOUDRON_MAIL_SMTP_SERVER
EMAIL_PORT = CLOUDRON_MAIL_SMTP_PORT
EMAIL_HOST_USER = CLOUDRON_MAIL_SMTP_USERNAME
EMAIL_HOST_PASSWORD = CLOUDRON_MAIL_SMTP_PASSWORD
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = CLOUDRON_MAIL_FROM

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = DATA_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

{% if cookiecutter.use_s3_storage == "yes" %}
# S3 Storage Configuration
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default=None)
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default=None)
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-1")
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN", default=None)
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

# Only use S3 in production
if not DEBUG and AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
{% endif %}

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = DATA_DIR / "media"

# Authentication
AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# django-allauth
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True

LOGIN_REDIRECT_URL = "home"
LOGIN_URL = "account_login"

# MFA Configuration
ACCOUNT_MFA_ENABLED = True
ACCOUNT_MFA_REQUIRED = False  # Set to True to force MFA
ACCOUNT_MFA_METHODS = ["authenticator"]

# Django Sites
SITE_ID = 1

{% if cookiecutter.use_cloudron_auth == "yes" %}
# Cloudron OpenID Connect Configuration
SOCIALACCOUNT_PROVIDERS = {
    "openid_connect": {
        "APPS": [
            {
                "provider_id": "cloudron",
                "name": "Cloudron",
                "client_id": env("CLOUDRON_OIDC_CLIENT_ID", default=""),
                "secret": env("CLOUDRON_OIDC_CLIENT_SECRET", default=""),
                "settings": {
                    "server_url": env("CLOUDRON_OIDC_ISSUER", default=""),
                },
            }
        ]
    }
}
{% endif %}

# Security Settings
SECURE_SSL_REDIRECT = env("DJANGO_SECURE_SSL_REDIRECT")
SECURE_HSTS_SECONDS = env("DJANGO_SECURE_HSTS_SECONDS")
SECURE_HSTS_INCLUDE_SUBDOMAINS = env("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS")
SECURE_HSTS_PRELOAD = env("DJANGO_SECURE_HSTS_PRELOAD")
SESSION_COOKIE_SECURE = env("DJANGO_SESSION_COOKIE_SECURE")
CSRF_COOKIE_SECURE = env("DJANGO_CSRF_COOKIE_SECURE")

# Content Security Policy
CONTENT_SECURITY_POLICY = {
    "EXCLUDE_URL_PREFIXES": ["/admin"],
    "DIRECTIVES": {
        "default-src": [SELF, "{{ cookiecutter.location }}"],
        "script-src": [SELF, "cdn.jsdelivr.net", "unpkg.com", "'unsafe-inline'"],
        "style-src": [SELF, "cdn.jsdelivr.net", "'unsafe-inline'"],
        "img-src": [SELF, "data:", "https:"],
    },
}

# CORS Settings
CORS_URLS_REGEX = r"^/api/.*$"
CORS_ALLOWED_ORIGINS = [
    CLOUDRON_APP_ORIGIN,
    "https://cdn.jsdelivr.net",
    "https://unpkg.com",
]

# Django Debug Toolbar
INTERNAL_IPS = ["127.0.0.1"]

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

{% if cookiecutter.use_scheduler == "yes" %}
# Celery Configuration
CELERY_BROKER_URL = (
    f"redis://:{env('CLOUDRON_REDIS_PASSWORD')}@{env('CLOUDRON_REDIS_HOST')}:{env('CLOUDRON_REDIS_PORT')}/0"
)
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
{% endif %}

# HTMX Settings
DJANGO_HTMX_REFRESH_TIMEOUT = 2000  # in milliseconds

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "_granian": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "granian": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "{{ cookiecutter.project_slug }}": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
