from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError


def validate_unique_username(value: str) -> None:
    if User.objects.filter(username=value).exists():
        raise ValidationError(_("A user with that username already exists."))
