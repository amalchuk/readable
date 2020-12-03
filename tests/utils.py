from secrets import token_hex
from typing import Callable

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import post_save
from django.test.testcases import TestCase as BaseTestCase

from readable.models import Documents
from readable.models import Staff
from readable.utils.signals import documents_uploaded
from readable.utils.signals import user_logged_in_out
from readable.utils.signals import user_staff_is_created


class TestCase(BaseTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super(TestCase, cls).setUpClass()
        post_save.disconnect(documents_uploaded, Documents)
        user_logged_in.disconnect(user_logged_in_out)
        user_logged_out.disconnect(user_logged_in_out)
        post_save.disconnect(user_staff_is_created, User)

    @classmethod
    def tearDownClass(cls) -> None:
        super(TestCase, cls).tearDownClass()
        post_save.connect(documents_uploaded, Documents)
        user_logged_in.connect(user_logged_in_out)
        user_logged_out.connect(user_logged_in_out)
        post_save.connect(user_staff_is_created, User)

    @staticmethod
    def get_random_string() -> str:
        return token_hex(25)

    @staticmethod
    def create_staff(user: User) -> Staff:
        staff, _ = Staff.objects.get_or_create(user=user)
        return staff

    @staticmethod
    def create_user(username: str, password: str, *, is_superuser: bool = False) -> User:
        create: Callable[..., User] = User.objects.create_superuser if is_superuser else User.objects.create_user
        return create(username=username, password=password)


get_random_string = TestCase.get_random_string
create_staff = TestCase.create_staff
create_user = TestCase.create_user
