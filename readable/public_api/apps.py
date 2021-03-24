from typing import Final

from django.apps.config import AppConfig
from django.utils.translation import gettext_lazy as _

__all__: Final[list[str]] = ["Configuration"]


class Configuration(AppConfig):
    name: str = "readable.public_api"
    verbose_name: str = _("Public REST API")
