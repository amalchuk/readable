from secrets import token_hex as get_random_string
from unicodedata import is_normalized

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from readable.forms import AuthenticationForm
from readable.forms import UserCreationForm


class TestAuthenticationForm(TestCase):
    def setUp(self) -> None:
        self.username = "future"
        self.password = get_random_string(25)
        User.objects.create_user(username=self.username, password=self.password)

    def test_clean_username(self) -> None:
        form = AuthenticationForm(data={
            "username": "\uFF26\uFF55\uFF54\uFF55\uFF52\uFF45",
            "password": self.password
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(is_normalized("NFKC", form.cleaned_data["username"]))
        self.assertTrue(form.cleaned_data["username"].islower())
        self.assertEqual(form.cleaned_data["username"], self.username)


class TestUserCreationForm(TestCase):
    def setUp(self) -> None:
        self.username = "TestCase"
        self.password = get_random_string()

    def test_clean_username(self) -> None:
        form = UserCreationForm(data={
            "username": self.username,
            "password1": self.password,
            "password2": self.password
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data["username"].islower())
