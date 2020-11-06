from unicodedata import is_normalized

from readable.forms import AuthenticationForm
from readable.forms import UserCreationForm
from tests.common import TestCase


class TestAuthenticationForm(TestCase):
    def setUp(self) -> None:
        super(TestAuthenticationForm, self).setUp()

        self.username = "future"
        self.password = self.get_random_string()
        self.create_user(username=self.username, password=self.password)

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
        super(TestUserCreationForm, self).setUp()

        self.username = "TestCase"
        self.password = self.get_random_string()

    def test_clean_username(self) -> None:
        form = UserCreationForm(data={
            "username": self.username,
            "password1": self.password,
            "password2": self.password
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data["username"].islower())
