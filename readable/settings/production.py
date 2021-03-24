from readable.settings.staging import *

# Core Settings:

ALLOWED_HOSTS = ["readable.pw", "www.readable.pw"]

CSRF_COOKIE_DOMAIN: str = "readable.pw"

CSRF_COOKIE_HTTPONLY: bool = True

CSRF_COOKIE_SECURE: bool = True

CSRF_TRUSTED_ORIGINS: list[str] = ALLOWED_HOSTS

SECURE_PROXY_SSL_HEADER: tuple[str, str] = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_DOMAIN: str = "readable.pw"

SESSION_COOKIE_HTTPONLY: bool = True

SESSION_COOKIE_SECURE: bool = True
