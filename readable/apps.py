from django.apps.config import AppConfig
from django.utils.translation import gettext_lazy as _

__all__ = ["Configuration"]


class Configuration(AppConfig):
    name: str = "readable"
    verbose_name: str = _("readable")

    def ready(self) -> None:
        from importlib import import_module
        import_module(f"{self.name}.utils.signals")
