from pathlib import PurePath as _P
from typing import Any, Dict, List, Optional, Tuple

from django.contrib.messages import constants as message_constants
from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _

from readable.utils.temporary import temporary_directory

# Common Settings:

BASE_DIR: _P = _P(__file__).parent.parent

RESOURCES_DIR: _P = BASE_DIR / "resources"

DEFAULT_DATE_FORMAT: str = r"%d.%m.%Y"  # 01.01.1999

DEFAULT_DATETIME_FORMAT: str = r"%d.%m.%Y %H:%M:%S"  # 01.01.1999 00:00:00

DEFAULT_TIME_FORMAT: str = r"%H:%M:%S"  # 00:00:00

DJANGO_STANDARD_LIBRARIES: List[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles"
]

DJANGO_THIRD_PARTY_LIBRARIES: List[str] = [
    "rest_framework"
]

DJANGO_FIRST_PARTY_LIBRARIES: List[str] = [
    "readable",
    "readable.public_api"
]

# Core Settings:

ALLOWED_HOSTS: List[str] = ["*"]

CACHES: Dict[str, Any] = {
    "default": {
        "BACKEND": "diskcache.djangocache.DjangoCache",
        "KEY_PREFIX": "default",
        "LOCATION": str(temporary_directory()),
        "OPTIONS": {
            "size_limit": 1024 * 1024 * 256  # 256 megabytes
        }
    },
    "session": {
        "BACKEND": "diskcache.djangocache.DjangoCache",
        "KEY_PREFIX": "session",
        "LOCATION": str(temporary_directory()),
        "OPTIONS": {
            "size_limit": 1024 * 1024 * 256  # 256 megabytes
        }
    }
}

CSRF_COOKIE_AGE: int = 3600 * 24 * 7  # 1 week

CSRF_COOKIE_NAME: str = "csrf_token"

DATABASES: Dict[str, Any] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(RESOURCES_DIR / "readable.db")
    }
}

DATA_UPLOAD_MAX_MEMORY_SIZE: Optional[int] = None

DATE_FORMAT: str = "d.m.Y"  # 01.01.1999

DATE_INPUT_FORMATS: List[str] = [DEFAULT_DATE_FORMAT]

DATETIME_FORMAT: str = "d.m.Y H:i:s"  # 01.01.1999 00:00:00

DATETIME_INPUT_FORMATS: List[str] = [DEFAULT_DATETIME_FORMAT]

FILE_UPLOAD_MAX_MEMORY_SIZE: int = 1024 * 1024 * 50  # 50 megabytes

FILE_UPLOAD_TEMP_DIR: str = str(temporary_directory())

FIRST_DAY_OF_WEEK: int = 1  # Monday

INSTALLED_APPS: List[str] = DJANGO_STANDARD_LIBRARIES + DJANGO_THIRD_PARTY_LIBRARIES + DJANGO_FIRST_PARTY_LIBRARIES

LANGUAGE_CODE: str = "ru"

LANGUAGES: List[Tuple[str, str]] = [
    ("ru", _("Russian")),
    ("en", _("English"))
]

LOCALE_PATHS: List[str] = [
    str(RESOURCES_DIR / "translations")
]

LOGGING: Dict[str, Any] = {
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
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False
        },
        "django.security.DisallowedHost": {
            "handlers": ["blank"],
            "propagate": False
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
}

MIDDLEWARE: List[str] = [
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

TEMPLATES: List[Dict[str, Any]] = [
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

TIME_INPUT_FORMATS: List[str] = [DEFAULT_TIME_FORMAT]

TIME_ZONE: str = "UTC"

USE_TZ: bool = True

WSGI_APPLICATION: str = "readable.wsgi.application"

# Authorization:

AUTH_PASSWORD_VALIDATORS: List[Dict[str, Any]] = [
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {
            "user_attributes": ["username"],
            "max_similarity": 0.667
        }
    }
]

LOGIN_REDIRECT_URL: str = "index"

LOGIN_URL: str = "login"

LOGOUT_REDIRECT_URL: str = "index"

PASSWORD_HASHERS: List[str] = ["readable.utils.hashers.SHA256PasswordHasher"]

# Messages:

MESSAGE_STORAGE: str = "django.contrib.messages.storage.session.SessionStorage"

MESSAGE_TAGS: Dict[int, str] = {
    message_constants.DEBUG: "alert-secondary",
    message_constants.INFO: "alert-info",
    message_constants.SUCCESS: "alert-success",
    message_constants.WARNING: "alert-warning",
    message_constants.ERROR: "alert-danger"
}

# Sessions:

SESSION_CACHE_ALIAS: str = "session"

SESSION_COOKIE_AGE: int = 3600 * 24 * 7  # 1 week

SESSION_COOKIE_NAME: str = "access_token"

SESSION_ENGINE: str = "django.contrib.sessions.backends.cache"

# Static Files:

MEDIA_ROOT: str = str(RESOURCES_DIR / "mediafiles")

MEDIA_URL: str = "/media/"

STATIC_ROOT: str = str(RESOURCES_DIR / "staticfiles")

STATIC_URL: str = "/static/"

STATICFILES_DIRS: List[str] = [
    str(RESOURCES_DIR / "assets")
]

# Django REST Framework Settings:

REST_FRAMEWORK_AUTHENTICATION_CLASSES: List[str] = ["rest_framework.authentication.BasicAuthentication"]

REST_FRAMEWORK_PAGINATION_CLASS: str = "rest_framework.pagination.PageNumberPagination"

REST_FRAMEWORK_PARSER_CLASSES: List[str] = [
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.MultiPartParser"
]

REST_FRAMEWORK_PERMISSION_CLASSES: List[str] = ["rest_framework.permissions.IsAuthenticated"]

REST_FRAMEWORK_RENDERER_CLASSES: List[str] = ["rest_framework.renderers.JSONRenderer"]

REST_FRAMEWORK_PAGE_SIZE: int = 10

REST_FRAMEWORK: Dict[str, Any] = {
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

# Miscellaneous:

READABLE_DOCUMENTS_PAGINATE_BY: int = REST_FRAMEWORK_PAGE_SIZE

READABLE_META_DESCRIPTION: str = _("This tool will quickly test the readability, spelling and grammar of your text")

READABLE_META_KEYWORDS: List[str] = [
    _("Add document"),
    _("Automated readability index"),
    _("Coleman-Liau index"),
    _("Document"),
    _("Flesch-Kincaid score"),
    _("Grammar"),
    _("Letters"),
    _("Overall score"),
    _("Readability"),
    _("Sentences"),
    _("Spelling"),
    _("Syllables"),
    _("Text Statistics"),
    _("Text"),
    _("Words")
]
