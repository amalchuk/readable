from typing import Any, Dict

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password as standard_validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from readable.public_api.validators import validate_unique_username as is_unique_username
from readable.utils.validators import validate_ascii_username as is_ascii_username

__all__ = ["UserCreateSerializer", "UserRetrieveUpdateSerializer"]


class UserCreateSerializer(ModelSerializer):
    username = CharField(label=_("Login"), min_length=6, max_length=50, validators=[is_ascii_username, is_unique_username])
    password = CharField(label=_("Password"), write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data: Dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)

    def validate_username(self, username: str) -> str:
        """
        All case-based characters of the username field will be lowercased.
        """
        return username.lower()

    def validate_password(self, password: str) -> str:
        """
        Validate whether the password meets all validator requirements.
        """
        initial_data: Dict[str, str] = self.get_initial()
        instance: User = User(**initial_data)
        instance.set_unusable_password()

        standard_validate_password(password, user=instance)
        return password


class UserRetrieveUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
