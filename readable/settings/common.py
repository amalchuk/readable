from pathlib import Path
from secrets import token_hex as get_random_string
from tempfile import mkdtemp as temporary_directory
from typing import Any, Dict, Final, Sequence, Tuple

from django.contrib.messages import constants as message_constants
from django.utils.translation import gettext_lazy as _

# Common Settings:

BASE_DIR = Path(__file__).parent.parent

RESOURCES_DIR = BASE_DIR.joinpath("resources").resolve(strict=True)

# Core Settings:

ALLOWED_HOSTS = ["*"]

CACHES: Final[Dict[str, Any]] = {
    "default": {
        "BACKEND": "diskcache.djangocache.DjangoCache",
        "KEY_FUNCTION": lambda key, key_prefix, version: f"{key}\x24{key_prefix}\x24{version}",
        "KEY_PREFIX": "default",
        "LOCATION": temporary_directory()
    },
    "session": {
        "BACKEND": "diskcache.djangocache.DjangoCache",
        "KEY_FUNCTION": lambda key, key_prefix, version: f"{key}\x24{key_prefix}\x24{version}",
        "KEY_PREFIX": "session",
        "LOCATION": temporary_directory()
    }
}

CSRF_COOKIE_AGE = SESSION_COOKIE_AGE = 604800  # 1 week

CSRF_COOKIE_NAME = "csrf_token"

DATABASES: Dict[str, Any] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": RESOURCES_DIR.joinpath("readable.db").as_posix()
    }
}

DATE_FORMAT = SHORT_DATE_FORMAT = "d.m.Y"

DATE_INPUT_FORMATS = [
    r"%d.%m.%Y"
]

DATETIME_FORMAT = SHORT_DATETIME_FORMAT = "d.m.Y H:i:s"

DATETIME_INPUT_FORMATS: Final[Sequence[str]] = [
    r"%d.%m.%Y %H:%M:%S",
    r"%d.%m.%Y %H:%M"
]

FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 megabytes

FIRST_DAY_OF_WEEK = 1

INSTALLED_APPS: Final[Sequence[str]] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "readable"
]

LANGUAGE_CODE: Final[str] = "ru"

LANGUAGES: Final[Sequence[Tuple[str, str]]] = [
    ("ru", _("Russian")),
    ("en", _("English"))
]

LOCALE_PATHS = [
    RESOURCES_DIR.joinpath("translations").as_posix()
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "generic": {
            "format": r"%(asctime)s %(levelname)s (%(name)s) at %(lineno)d:%(filename)s in %(funcName)s: %(message)s",
            "datefmt": r"%d.%m.%Y %H:%M:%S"
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
            "level": "INFO"
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

MIDDLEWARE: Final[Sequence[str]] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
]

ROOT_URLCONF: Final[str] = "readable.urls"

SECRET_KEY = get_random_string(25)

TEMPLATES = [
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

TIME_INPUT_FORMATS: Final[Sequence[str]] = [
    r"%H:%M:%S",
    r"%H:%M"
]

TIME_ZONE = "UTC"

USE_TZ = True

# Authorization:

AUTH_PASSWORD_VALIDATORS = [
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

LOGIN_REDIRECT_URL = LOGOUT_REDIRECT_URL = "index"

LOGIN_URL = "login"

PASSWORD_HASHERS: Final[Sequence[str]] = ["readable.utils.hashers.SHA256PasswordHasher"]

# Messages:

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

MESSAGE_TAGS = {
    message_constants.DEBUG: "alert-secondary",
    message_constants.INFO: "alert-info",
    message_constants.SUCCESS: "alert-success",
    message_constants.WARNING: "alert-warning",
    message_constants.ERROR: "alert-danger"
}

# Sessions:

SESSION_CACHE_ALIAS = "session"

SESSION_COOKIE_NAME = "access_token"

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Static Files:

MEDIA_ROOT = RESOURCES_DIR.joinpath("mediafiles").as_posix()

MEDIA_URL = "/media/"

STATIC_ROOT = RESOURCES_DIR.joinpath("staticfiles").as_posix()

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    RESOURCES_DIR.joinpath("assets").as_posix()
]

# Miscellaneous:

READABLE_DOCUMENTS_PAGINATE_BY = 10

READABLE_META_DESCRIPTION = _("This tool will quickly test the readability, spelling and grammar of your text")

READABLE_META_KEYWORDS = [
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
