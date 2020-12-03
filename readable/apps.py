from django.apps.config import AppConfig
from django.utils.translation import gettext_lazy as _


class Configuration(AppConfig):
    name = "readable"
    verbose_name = _("readable")

    def ready(self) -> None:
        from importlib import import_module
        import_module(f"{self.name}.utils.signals")
