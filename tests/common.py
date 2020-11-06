from secrets import token_hex
from typing import Callable, Tuple

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import post_save
from django.test.testcases import TestCase as BaseTestCase

from readable.models import Documents
from readable.models import Staff
from readable.utils.signals import documents_uploaded
from readable.utils.signals import user_logged_in_out


class TestCase(BaseTestCase):
    def setUp(self) -> None:
        post_save.disconnect(documents_uploaded, Documents)
        user_logged_in.disconnect(user_logged_in_out)
        user_logged_out.disconnect(user_logged_in_out)

    def tearDown(self) -> None:
        post_save.connect(documents_uploaded, Documents)
        user_logged_in.connect(user_logged_in_out)
        user_logged_out.connect(user_logged_in_out)

    @classmethod
    def get_random_string(cls) -> str:
        return token_hex(25)

    @classmethod
    def create_user(cls, *, username: str, password: str, is_superuser: bool = False) -> Tuple[User, Staff]:
        create: Callable[..., User] = User.objects.create_superuser if is_superuser else User.objects.create_user
        user = create(username=username, password=password)
        return user, Staff.objects.create(user=user)
