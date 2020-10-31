from secrets import token_hex as get_random_string

from django.contrib.auth.models import User
from django.contrib.messages.api import get_messages
from django.contrib.messages.storage.base import Message
from django.http.response import HttpResponse
from django.test.testcases import TestCase
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _

from readable.models import Staff


class TestLogoutView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="staff", password="staff")
        self.staff = Staff.objects.create(user=self.user, user_agent="Mozilla/5.0", ip_address="127.0.0.1")
        self.client.force_login(self.user)

    def test_get_next_page(self) -> None:
        response: HttpResponse = self.client.get(reverse("logout"))
        message: Message = next(i for i in get_messages(response.wsgi_request))
        self.assertEqual(str(message), _("You have successfully logged out."))
        self.assertRedirects(response, reverse("index"))


class TestRegistrationView(TestCase):
    def setUp(self) -> None:
        self.username = "future"
        self.password = get_random_string(25)

    def test_form_valid(self) -> None:
        response: HttpResponse = self.client.post(reverse("registration"), data={
            "username": self.username,
            "password1": self.password,
            "password2": self.password
        })
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, self.username)


class TestDocumentsDetailView(TestCase):
    def setUp(self) -> None:
        # TODO: In Progress
        pass


class TestIndexView(TestCase):
    def setUp(self) -> None:
        # TODO: In Progress
        pass


class ProfileViewView(TestCase):
    def setUp(self) -> None:
        # TODO: In Progress
        pass
