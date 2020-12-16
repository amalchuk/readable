from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError

__all__ = ["validate_unique_username"]


def validate_unique_username(username: str) -> None:
    """
    Ensure that the ``username`` is unique.
    """
    if type(username) == str and User.objects.filter(username__iexact=username).exists():
        raise ValidationError(_("The username already exists. Please use a different username."))
