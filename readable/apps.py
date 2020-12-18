from typing import List

from django.apps.config import AppConfig
from django.utils.translation import gettext_lazy as _

__all__: List[str] = ["Configuration"]


class Configuration(AppConfig):
    name: str = "readable"
    verbose_name: str = _("readable")

    def ready(self) -> None:
        import readable.utils.signals
