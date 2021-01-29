from importlib import import_module
from typing import Final, List

from django.apps.config import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

__all__: Final[List[str]] = ["Configuration"]


class Configuration(AppConfig):
    name: str = "readable"
    verbose_name: str = _("readable")

    def ready(self) -> None:
        import_module(settings.READABLE_SIGNALS_MODULE)
