from typing import Any, Dict

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from readable.api.validators import validate_unique_username as is_unique_username
from readable.models import Staff
from readable.utils.validators import validate_ascii_username as is_ascii_username

__all__ = ["UserCreateSerializer", "UserRetrieveUpdateSerializer"]


class UserCreateSerializer(ModelSerializer):
    username = CharField(label=_("Login"), min_length=6, max_length=50, validators=[is_ascii_username, is_unique_username])
    password = CharField(label=_("Password"), write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data: Dict[str, Any]) -> User:
        instance: User = User.objects.create_user(**validated_data)
        Staff.objects.update_or_create(user=instance)
        return instance


class UserRetrieveUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
