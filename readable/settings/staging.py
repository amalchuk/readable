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
        "OPTIONS": {  # type: ignore
            "CLIENT_CLASS": "django_redis.client.default.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",
            "CONNECTION_POOL_KWARGS": {
                "health_check_interval": 1800,
                "max_connections": 4096,
                "retry_on_timeout": True
            }
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {  # type: ignore
            "CLIENT_CLASS": "django_redis.client.default.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",
            "CONNECTION_POOL_KWARGS": {
                "health_check_interval": 1800,
                "max_connections": 4096,
                "retry_on_timeout": True
            }
        }
    },
    "internal": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/2",
        "OPTIONS": {  # type: ignore
            "CLIENT_CLASS": "django_redis.client.default.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",
            "CONNECTION_POOL_KWARGS": {
                "health_check_interval": 1800,
                "max_connections": 4096,
                "retry_on_timeout": True
            }
        }
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": environ["POSTGRESQL_USER"],
        "PASSWORD": environ["POSTGRESQL_PASSWORD"],
        "HOST": "postgresql",
        "PORT": "5432",
        "NAME": environ["POSTGRESQL_DATABASE"],
        "OPTIONS": {  # type: ignore
            "isolation_level": import_string("psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE")
        }
    }
}

SECRET_KEY = environ.get("DJANGO_SECRET_KEY", SECRET_KEY)

USE_X_FORWARDED_HOST = True

# Sessions:

SESSION_CACHE_ALIAS = "session"

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Miscellaneous:

READABLE_INTERNAL_CACHE_ALIAS = "internal"
