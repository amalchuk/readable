from os import environ

from django.utils.module_loading import import_string

from readable.settings.common import *

# Core Settings:

ADMINS: list[tuple[str, str]] = [
    ("Andrew Malchuk", "andrew.malchuk@yandex.ru"),
    ("webmaster", "webmaster@readable.pw")
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": environ["POSTGRES_USER"],
        "PASSWORD": environ["POSTGRES_PASSWORD"],
        "HOST": "postgresql",
        "PORT": "5432",
        "NAME": environ["POSTGRES_DB"],
        "OPTIONS": {
            "isolation_level": import_string("psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE")
        }
    }
}

SECRET_KEY = environ.get("DJANGO_SECRET_KEY", SECRET_KEY)

USE_X_FORWARDED_HOST: bool = True
