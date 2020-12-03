from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny

from readable.public_api.serializers.users import UserCreateSerializer
from readable.public_api.serializers.users import UserRetrieveUpdateSerializer

__all__ = ["user_create_view", "user_retrieve_update_view"]


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserRetrieveUpdateSerializer

    def get_object(self) -> User:
        return self.request.user


user_create_view = UserCreateAPIView.as_view()
user_retrieve_update_view = UserRetrieveUpdateAPIView.as_view()
