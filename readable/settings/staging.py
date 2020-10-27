from os import environ

from django.utils.module_loading import import_string

from readable.settings.common import *

# Core Settings:

ADMINS = [
    ("Andrew Malchuk", "andrew.malchuk@yandex.ru")
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.default.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",
            "CONNECTION_POOL_KWARGS": {
                "health_check_interval": 1800,
                "retry_on_timeout": True
            }
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.default.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",
            "CONNECTION_POOL_KWARGS": {
                "health_check_interval": 1800,
                "retry_on_timeout": True
            }
        }
    }
}

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

USE_X_FORWARDED_HOST = True

# Sessions:

SESSION_CACHE_ALIAS = "session"

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Static Files:

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
