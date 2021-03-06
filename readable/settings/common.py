from datetime import timedelta
from pathlib import PurePath as _P
from typing import Any, Optional

from django.contrib.messages import constants as message_constants
from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _

from readable.utils.collections import as_list
from readable.utils.temporary import temporary_directory

# Common Settings:

BASE_DIR: _P = _P(__file__).parent.parent

RESOURCES_DIR: _P = BASE_DIR / "resources"

DEFAULT_DATE_FORMAT: str = r"%d.%m.%Y"  # 01.01.1999

DEFAULT_DATETIME_FORMAT: str = r"%d.%m.%Y %H:%M:%S"  # 01.01.1999 00:00:00

DEFAULT_TIME_FORMAT: str = r"%H:%M:%S"  # 00:00:00

DJANGO_STANDARD_LIBRARIES: list[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles"
]

DJANGO_THIRD_PARTY_LIBRARIES: list[str] = [
    "rest_framework"
]

DJANGO_FIRST_PARTY_LIBRARIES: list[str] = [
    "readable",
    "readable.public_api"
]

# Core Settings:

ALLOWED_HOSTS: list[str] = as_list("\x2A")

CACHES: dict[str, Any] = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "KEY_PREFIX": "default\x5F",
        "LOCATION": temporary_directory(prefix="readable\x2Ddefault\x2D").as_posix()
    },
    "session": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "KEY_PREFIX": "session\x5F",
        "LOCATION": temporary_directory(prefix="readable\x2Dsession\x2D").as_posix()
    }
}

CSRF_COOKIE_AGE: float = timedelta(weeks=1).total_seconds()

CSRF_COOKIE_NAME: str = "csrf_token"

DATABASES: dict[str, Any] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": (RESOURCES_DIR / "readable.db").as_posix()
    }
}

DATA_UPLOAD_MAX_MEMORY_SIZE: Optional[int] = None

DATE_FORMAT: str = "d.m.Y"  # 01.01.1999

DATE_INPUT_FORMATS: list[str] = as_list(DEFAULT_DATE_FORMAT)

DATETIME_FORMAT: str = "d.m.Y H:i:s"  # 01.01.1999 00:00:00

DATETIME_INPUT_FORMATS: list[str] = as_list(DEFAULT_DATETIME_FORMAT)

FILE_UPLOAD_MAX_MEMORY_SIZE: int = 1024 * 1024 * 50  # 50 megabytes

FILE_UPLOAD_TEMP_DIR: str = temporary_directory(prefix="readable\x2Dupload\x2D").as_posix()

FIRST_DAY_OF_WEEK: int = 1  # Monday

INSTALLED_APPS: list[str] = DJANGO_STANDARD_LIBRARIES + DJANGO_THIRD_PARTY_LIBRARIES + DJANGO_FIRST_PARTY_LIBRARIES

LANGUAGE_CODE: str = "ru"

LANGUAGES: list[tuple[str, str]] = [
    ("ru", _("Russian")),
    ("en", _("English"))
]

LOCALE_PATHS: list[str] = as_list((RESOURCES_DIR / "translations").as_posix())

LOGGING: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "generic": {
            "format": r"%(asctime)s %(levelname)s (%(name)s) at %(lineno)d:%(filename)s in %(funcName)s: %(message)s",
            "datefmt": DEFAULT_DATETIME_FORMAT
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": "ext://sys.stdout"
        },
        "blank": {
            "class": "logging.NullHandler"
        }
    },
    "loggers": {
        "django": {
            "handlers": as_list("console"),
            "level": "INFO",
            "propagate": False
        },
        "django.request": {
            "handlers": as_list("console"),
            "level": "ERROR",
            "propagate": False
        },
        "django.security.DisallowedHost": {
            "handlers": as_list("blank"),
            "propagate": False
        }
    },
    "root": {
        "handlers": as_list("console"),
        "level": "INFO"
    }
}

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
]

ROOT_URLCONF: str = "readable.urls"

SECRET_KEY: str = get_random_secret_key()

SHORT_DATE_FORMAT: str = "d.m.Y"  # 01.01.1999

SHORT_DATETIME_FORMAT: str = "d.m.Y H:i:s"  # 01.01.1999 00:00:00

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request"
            ]
        }
    }
]

TIME_FORMAT: str = "H:i:s"  # 00:00:00

TIME_INPUT_FORMATS: list[str] = as_list(DEFAULT_TIME_FORMAT)

TIME_ZONE: str = "UTC"

USE_TZ: bool = True

WSGI_APPLICATION: str = "readable.wsgi.application"

# Authorization:

AUTH_PASSWORD_VALIDATORS: list[dict[str, Any]] = [
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {
            "user_attributes": as_list("username"),
            "max_similarity": 0.5
        }
    }
]

LOGIN_REDIRECT_URL: str = "index"

LOGIN_URL: str = "login"

LOGOUT_REDIRECT_URL: str = "index"

PASSWORD_HASHERS: list[str] = as_list("readable.utils.hashers.SHA256PasswordHasher")

# Messages:

MESSAGE_STORAGE: str = "django.contrib.messages.storage.session.SessionStorage"

MESSAGE_TAGS: dict[int, str] = {
    message_constants.DEBUG: "alert-secondary",
    message_constants.INFO: "alert-info",
    message_constants.SUCCESS: "alert-success",
    message_constants.WARNING: "alert-warning",
    message_constants.ERROR: "alert-danger"
}

# Sessions:

SESSION_CACHE_ALIAS: str = "session"

SESSION_COOKIE_AGE: float = timedelta(weeks=1).total_seconds()

SESSION_COOKIE_NAME: str = "access_token"

SESSION_ENGINE: str = "django.contrib.sessions.backends.cache"

# Static Files:

MEDIA_ROOT: str = (RESOURCES_DIR / "mediafiles").as_posix()

MEDIA_URL: str = "/media/"

STATIC_ROOT: str = (RESOURCES_DIR / "staticfiles").as_posix()

STATIC_URL: str = "/static/"

STATICFILES_DIRS: list[str] = as_list((RESOURCES_DIR / "assets").as_posix())

# Django REST Framework Settings:

REST_FRAMEWORK_AUTHENTICATION_CLASSES: list[str] = as_list("rest_framework.authentication.BasicAuthentication")

REST_FRAMEWORK_PAGINATION_CLASS: str = "rest_framework.pagination.PageNumberPagination"

REST_FRAMEWORK_PARSER_CLASSES: list[str] = as_list("rest_framework.parsers.JSONParser")

REST_FRAMEWORK_PERMISSION_CLASSES: list[str] = as_list("rest_framework.permissions.IsAuthenticated")

REST_FRAMEWORK_RENDERER_CLASSES: list[str] = as_list("rest_framework.renderers.JSONRenderer")

REST_FRAMEWORK_PAGE_SIZE: int = 10

REST_FRAMEWORK: dict[str, Any] = {
    "DATE_FORMAT": DEFAULT_DATE_FORMAT,
    "DATE_INPUT_FORMATS": DATE_INPUT_FORMATS,
    "DATETIME_FORMAT": DEFAULT_DATETIME_FORMAT,
    "DATETIME_INPUT_FORMATS": DATETIME_INPUT_FORMATS,
    "DEFAULT_AUTHENTICATION_CLASSES": REST_FRAMEWORK_AUTHENTICATION_CLASSES,
    "DEFAULT_PAGINATION_CLASS": REST_FRAMEWORK_PAGINATION_CLASS,
    "DEFAULT_PARSER_CLASSES": REST_FRAMEWORK_PARSER_CLASSES,
    "DEFAULT_PERMISSION_CLASSES": REST_FRAMEWORK_PERMISSION_CLASSES,
    "DEFAULT_RENDERER_CLASSES": REST_FRAMEWORK_RENDERER_CLASSES,
    "PAGE_SIZE": REST_FRAMEWORK_PAGE_SIZE,
    "TIME_FORMAT": DEFAULT_TIME_FORMAT,
    "TIME_INPUT_FORMATS": TIME_INPUT_FORMATS
}
