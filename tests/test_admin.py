from http import HTTPStatus
from typing import Optional, Sequence

from django.contrib.admin.options import InlineModelAdmin
from django.core.files.base import ContentFile
from django.http.response import HttpResponse
from django.urls.base import reverse

from readable.models import Documents
from readable.models import Metrics
from readable.models import Staff
from tests.common import TestCase


class TestUserAdmin(TestCase):
    def setUp(self) -> None:
        super(TestUserAdmin, self).setUp()
        self.response: HttpResponse
        self.inlines: Sequence[InlineModelAdmin]

        self.user, _ = self.create_user(username="staff", password=self.get_random_string(), is_superuser=True)
        self.client.force_login(self.user)

    def test_get_inlines(self) -> None:
        self.response = self.client.get(reverse("admin:auth_user_add"))
        self.inlines = self.response.context["inline_admin_formsets"]
        self.assertIsInstance(self.inlines, Sequence)
        self.assertTrue(len(self.inlines) == 0)

        self.response = self.client.get(reverse("admin:auth_user_change", args=[self.user.id]))
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

        self.inlines = self.response.context["inline_admin_formsets"]
        self.assertTrue(len(self.inlines) == 1)
        self.assertIs(self.inlines[0].opts.model, Staff)


class TestDocumentsAdmin(TestCase):
    def setUp(self) -> None:
        super(TestDocumentsAdmin, self).setUp()
        self.response: HttpResponse
        self.inlines: Sequence[InlineModelAdmin]

        self.user, self.staff = self.create_user(username="staff", password=self.get_random_string(), is_superuser=True)
        self.client.force_login(self.user)
        self.lorem = ContentFile("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "lorem.txt")

    def test_get_inlines(self) -> None:
        self.response = self.client.get(reverse("admin:readable_documents_add"))
        self.inlines = self.response.context["inline_admin_formsets"]
        self.assertIsInstance(self.inlines, Sequence)
        self.assertTrue(len(self.inlines) == 0)

        document: Documents = Documents.objects.create(filename=self.lorem, uploaded_by=self.staff)
        self.response = self.client.get(reverse("admin:readable_documents_change", args=[document.id]))
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

        self.inlines = self.response.context["inline_admin_formsets"]
        self.assertTrue(len(self.inlines) == 1)
        self.assertIs(self.inlines[0].opts.model, Metrics)

    def test_save_model(self) -> None:
        self.response = self.client.post(reverse("admin:readable_documents_add"), data={
            "filename": self.lorem
        })
        self.assertRedirects(self.response, reverse("admin:readable_documents_changelist"))

        document: Optional[Documents] = Documents.objects.first()
        self.assertIsNotNone(document)
        self.assertEqual(document.uploaded_by, self.staff)  # type: ignore
