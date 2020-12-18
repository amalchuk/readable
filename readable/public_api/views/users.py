from typing import Callable, List

from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from readable.public_api.serializers.users import UserCreateSerializer
from readable.public_api.serializers.users import UserRetrieveUpdateSerializer

__all__: List[str] = ["user_create_view", "user_retrieve_update_view"]


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserRetrieveUpdateSerializer

    def get_object(self) -> User:
        return self.request.user


user_create_view: Callable[..., Response] = UserCreateAPIView.as_view()
user_retrieve_update_view: Callable[..., Response] = UserRetrieveUpdateAPIView.as_view()
