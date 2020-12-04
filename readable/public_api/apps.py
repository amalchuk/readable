from django.apps.config import AppConfig
from django.utils.translation import gettext_lazy as _


class Configuration(AppConfig):
    name = "readable.public_api"
    verbose_name = _("Public REST API")
