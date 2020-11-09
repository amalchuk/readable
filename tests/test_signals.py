from secrets import token_hex as get_random_string
from typing import Dict, Type

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.core.handlers.wsgi import WSGIRequest
from django.test.client import RequestFactory
from django.test.testcases import TestCase
from django.urls.base import reverse

from readable.models import Staff

from .common import TestCase as CommonTestCase


class TestUserLoggedInOut(TestCase):
    def setUp(self) -> None:
        self.username = "staff"
        self.password = CommonTestCase.get_random_string()
        self.user = CommonTestCase.create_user(username=self.username, password=self.password)
        self.factory = RequestFactory()

    def test_login(self) -> None:
        defaults: Dict[str, str] = {
            "HTTP_USER_AGENT": "Mozilla/5.0 TestCase/Login",
            "REMOTE_ADDR": "127.0.0.1"
        }
        request: WSGIRequest = self.factory.post(reverse("admin:login"), data={
            "username": self.username,
            "password": self.password
        }, **defaults)
        sender: Type[User] = getattr(self.user, "__class__")

        user_logged_in.send(sender=sender, request=request, user=self.user)
        self.assertTrue(Staff.objects.filter(user=self.user).exists())

        staff: Staff = Staff.objects.get(user=self.user)
        self.assertEqual(staff.user_agent, defaults["HTTP_USER_AGENT"])
        self.assertEqual(staff.ip_address, defaults["REMOTE_ADDR"])

    def test_logout(self) -> None:
        defaults: Dict[str, str] = {
            "HTTP_USER_AGENT": "Mozilla/5.0 TestCase/Logout",
            "REMOTE_ADDR": "127.0.0.1"
        }
        request: WSGIRequest = self.factory.post(reverse("admin:logout"), **defaults)
        request.user = self.user
        sender: Type[User] = getattr(self.user, "__class__")

        user_logged_out.send(sender=sender, request=request, user=self.user)
        self.assertTrue(Staff.objects.filter(user=self.user).exists())

        staff: Staff = Staff.objects.get(user=self.user)
        self.assertEqual(staff.user_agent, defaults["HTTP_USER_AGENT"])
        self.assertEqual(staff.ip_address, defaults["REMOTE_ADDR"])
