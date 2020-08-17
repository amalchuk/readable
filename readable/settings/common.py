from pathlib import Path
from secrets import token_hex as get_random_string

from django.contrib.messages import constants as message_constants
from django.utils.translation import gettext_lazy as _

from readable.utils.executors import ThreadPoolExecutor

# Common Settings:

BASE_DIR = Path(__file__).parent.parent

RESOURCES_DIR = (BASE_DIR / "resources").resolve(strict=True)

# Core Settings:

ALLOWED_HOSTS = ["*"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache"
    }
}

CSRF_COOKIE_AGE = SESSION_COOKIE_AGE = 604800  # 1 week

CSRF_COOKIE_NAME = "csrf_token"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": (RESOURCES_DIR / "readable.db").as_posix()
    }
}

DATE_FORMAT = SHORT_DATE_FORMAT = "d.m.Y"

DATE_INPUT_FORMATS = [
    r"%d.%m.%Y"
]

DATETIME_FORMAT = SHORT_DATETIME_FORMAT = "d.m.Y H:i:s"

DATETIME_INPUT_FORMATS = [
    r"%d.%m.%Y %H:%M:%S",
    r"%d.%m.%Y %H:%M"
]

FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 megabytes

FIRST_DAY_OF_WEEK = 1

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "readable"
]

LANGUAGE_CODE = "ru"

LANGUAGES = [
    ("ru", _("Russian")),
    ("en", _("English"))
]

LOCALE_PATHS = [
    (RESOURCES_DIR / "translations").as_posix()
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
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO"
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
]

ROOT_URLCONF = "readable.urls"

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

TIME_INPUT_FORMATS = [
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

PASSWORD_HASHERS = ["readable.utils.hashers.SHA256PasswordHasher"]

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

SESSION_COOKIE_NAME = "access_token"

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# Static Files:

MEDIA_ROOT = (RESOURCES_DIR / "mediafiles").as_posix()

MEDIA_URL = "/media/"

STATIC_ROOT = (RESOURCES_DIR / "staticfiles").as_posix()

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    (RESOURCES_DIR / "assets").as_posix()
]

# Miscellaneous:

READABLE_DOCUMENTS_PAGINATE_BY = 10

READABLE_INTERNAL_CACHE_ALIAS = "default"

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

READABLE_POOL_EXECUTOR = ThreadPoolExecutor()  # type: ignore
