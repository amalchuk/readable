from typing import Final

from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
from rest_framework.serializers import BaseSerializer

from readable.public_api.serializers.users import UserCreateSerializer
from readable.public_api.serializers.users import UserRetrieveUpdateSerializer
from readable.types import ViewType
from readable.utils.collections import as_list

__all__: Final[list[str]] = ["user_create_view", "user_retrieve_update_view"]


class UserCreateAPIView(CreateAPIView):
    permission_classes: list[type[BasePermission]] = as_list(AllowAny)
    serializer_class: type[BaseSerializer] = UserCreateSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class: type[BaseSerializer] = UserRetrieveUpdateSerializer

    def get_object(self) -> User:
        return self.request.user


user_create_view: Final[ViewType] = UserCreateAPIView.as_view()
user_retrieve_update_view: Final[ViewType] = UserRetrieveUpdateAPIView.as_view()
