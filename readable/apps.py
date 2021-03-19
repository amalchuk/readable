from typing import Final

from django.apps.config import AppConfig
from django.apps.registry import apps
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

__all__: Final[list[str]] = ["Configuration"]


class Configuration(AppConfig):
    name: str = "readable"
    verbose_name: str = _("readable")

    def ready(self) -> None:
        from readable.utils.signals import documents_uploaded
        post_save.connect(documents_uploaded, self.get_model("Documents"))

        from readable.utils.signals import user_logged_in_out
        user_logged_in.connect(user_logged_in_out)
        user_logged_out.connect(user_logged_in_out)

        from readable.utils.signals import user_staff_is_created
        post_save.connect(user_staff_is_created, apps.get_registered_model("auth", "User"))
