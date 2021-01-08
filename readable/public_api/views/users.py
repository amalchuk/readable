from typing import Callable, List, Type

from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from readable.public_api.serializers.users import UserCreateSerializer
from readable.public_api.serializers.users import UserRetrieveUpdateSerializer
from readable.utils.collections import as_list

__all__: List[str] = ["user_create_view", "user_retrieve_update_view"]


class UserCreateAPIView(CreateAPIView):
    permission_classes: List[Type[BasePermission]] = as_list(AllowAny)
    serializer_class: Type[BaseSerializer] = UserCreateSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class: Type[BaseSerializer] = UserRetrieveUpdateSerializer

    def get_object(self) -> User:
        return self.request.user


user_create_view: Callable[..., Response] = UserCreateAPIView.as_view()
user_retrieve_update_view: Callable[..., Response] = UserRetrieveUpdateAPIView.as_view()
