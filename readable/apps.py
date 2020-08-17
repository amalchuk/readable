from django.apps.config import AppConfig
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _


class Configuration(AppConfig):
    name = "readable"
    verbose_name = _("readable")

    def ready(self) -> None:
        from readable.utils.signals import documents_uploaded
        post_save.connect(documents_uploaded, self.get_model("Documents"))

        from readable.utils.signals import user_logged_in_out
        user_logged_in.connect(user_logged_in_out)
        user_logged_out.connect(user_logged_in_out)
