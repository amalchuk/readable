from http import HTTPStatus
from secrets import token_hex as get_random_string

from django.contrib.auth.models import User
from django.contrib.messages.api import get_messages
from django.contrib.messages.storage.base import Message
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.http.response import HttpResponse
from django.test.testcases import TestCase
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _

from readable.models import Documents
from readable.models import Staff
from readable.utils.signals import documents_uploaded


class TestLogoutView(TestCase):
    def setUp(self) -> None:
        self.response: HttpResponse
        self.user: User = User.objects.create_user(username="staff", password="staff")
        self.staff: Staff = Staff.objects.create(user=self.user)
        self.client.force_login(self.user)

    def test_get_next_page(self) -> None:
        self.response = self.client.get(reverse("logout"))
        message: Message = next(i for i in get_messages(self.response.wsgi_request))
        self.assertEqual(str(message), _("You have successfully logged out."))
        self.assertRedirects(self.response, reverse("index"))


class TestRegistrationView(TestCase):
    def setUp(self) -> None:
        self.response: HttpResponse
        self.username: str = "future"
        self.password: str = get_random_string(25)

    def test_form_valid(self) -> None:
        self.response = self.client.post(reverse("registration"), data={
            "username": self.username,
            "password1": self.password,
            "password2": self.password
        })
        self.assertTrue(self.response.wsgi_request.user.is_authenticated)
        self.assertEqual(self.response.wsgi_request.user.username, self.username)
        self.assertRedirects(self.response, reverse("index"))


class TestDocumentsDetailView(TestCase):
    def setUp(self) -> None:
        self.response: HttpResponse

        self.user1: User = User.objects.create_user(username="staff1", password="staff1")
        self.staff1: Staff = Staff.objects.create(user=self.user1)
        self.client.force_login(self.user1)

        self.user2: User = User.objects.create_user(username="staff2", password="staff2")
        self.staff2: Staff = Staff.objects.create(user=self.user2)

    def test_get_queryset(self) -> None:
        # Temporarily disable the "documents_uploaded" signal:
        post_save.disconnect(documents_uploaded, Documents)

        self.response = self.client.post(reverse("index"), data={
            "filename": ContentFile("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "lorem.txt")
        })
        self.assertRedirects(self.response, reverse("index"))

        document: Documents = Documents.objects.get(uploaded_by=self.staff1)
        self.response = self.client.get(reverse("documents_detail", args=[document.id]))
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

        document.uploaded_by = self.staff2
        document.save(update_fields=["uploaded_by"])
        self.response = self.client.get(reverse("documents_detail", args=[document.id]))
        self.assertEqual(self.response.status_code, HTTPStatus.NOT_FOUND)


class TestProfileView(TestCase):
    def setUp(self) -> None:
        self.response: HttpResponse
        self.user: User = User.objects.create_user(username="staff", password="staff")
        self.staff: Staff = Staff.objects.create(user=self.user)
        self.client.force_login(self.user)

    def test_form_valid(self) -> None:
        self.response = self.client.post(reverse("profile"), data={
            "first_name": "John",
            "last_name": "Doe"
        })
        message: Message = next(i for i in get_messages(self.response.wsgi_request))
        self.assertEqual(str(message), _("Your account has been successfully updated."))
        self.assertRedirects(self.response, reverse("profile"))
        self.assertEqual(self.response.wsgi_request.user.first_name, "John")
        self.assertEqual(self.response.wsgi_request.user.last_name, "Doe")

    def test_get_object(self) -> None:
        self.response = self.client.get(reverse("profile"))
        self.assertEqual(self.response.context["object"], self.user)
