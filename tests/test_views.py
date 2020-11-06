from http import HTTPStatus
import logging

from django.contrib.messages.api import get_messages
from django.contrib.messages.storage.base import Message
from django.core.files.base import ContentFile
from django.http.response import HttpResponse
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _

from readable.models import Documents
from tests.common import TestCase


class TestLogoutView(TestCase):
    def setUp(self) -> None:
        super(TestLogoutView, self).setUp()
        self.response: HttpResponse

        self.user, _ = self.create_user(username="staff", password=self.get_random_string())
        self.client.force_login(self.user)

    def test_get_next_page(self) -> None:
        self.response = self.client.get(reverse("logout"))
        message: Message = next(i for i in get_messages(self.response.wsgi_request))
        self.assertEqual(str(message), _("You have successfully logged out."))
        self.assertRedirects(self.response, reverse("index"))


class TestRegistrationView(TestCase):
    def setUp(self) -> None:
        super(TestRegistrationView, self).setUp()
        self.response: HttpResponse

        self.username = "future"
        self.password = self.get_random_string()

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
        super(TestDocumentsDetailView, self).setUp()
        self.response: HttpResponse
        logging.disable(logging.WARNING)

        self.user1, self.staff1 = self.create_user(username="staff1", password=self.get_random_string())
        _, self.staff2 = self.create_user(username="staff2", password=self.get_random_string())
        self.client.force_login(self.user1)
        self.lorem = ContentFile("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "lorem.txt")

    def test_get_queryset(self) -> None:
        self.response = self.client.post(reverse("index"), data={
            "filename": self.lorem
        })
        self.assertRedirects(self.response, reverse("index"))

        document: Documents = Documents.objects.get(uploaded_by=self.staff1)
        self.response = self.client.get(reverse("documents_detail", args=[document.id]))
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

        document.uploaded_by = self.staff2
        document.save(update_fields=["uploaded_by"])
        self.response = self.client.get(reverse("documents_detail", args=[document.id]))
        self.assertEqual(self.response.status_code, HTTPStatus.NOT_FOUND)

    def tearDown(self) -> None:
        super(TestDocumentsDetailView, self).tearDown()
        logging.disable(logging.NOTSET)


class TestProfileView(TestCase):
    def setUp(self) -> None:
        super(TestProfileView, self).setUp()
        self.response: HttpResponse

        self.user, _ = self.create_user(username="staff", password=self.get_random_string())
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
