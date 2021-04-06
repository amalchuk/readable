from http import HTTPStatus
from typing import Optional, Sequence, cast

from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.base import File
from django.http.response import HttpResponse
from django.urls.base import reverse

from readable.models import Documents
from readable.models import Metrics
from readable.models import Staff
from readable.utils.collections import as_list

from .utils import TestCase


class TestUserAdmin(TestCase):
    response: HttpResponse
    inlines: Sequence[InlineModelAdmin]

    def setUp(self) -> None:
        super(TestUserAdmin, self).setUp()
        self.user: User = self.create_user("staff", self.get_random_string(), is_superuser=True)
        self.client.force_login(self.user)

    def test_get_inlines(self) -> None:
        self.response = self.client.get(reverse("admin:auth_user_add"))
        self.inlines = self.response.context["inline_admin_formsets"]
        self.assertIsInstance(self.inlines, Sequence)
        self.assertTrue(len(self.inlines) == 0)

        self.response = self.client.get(reverse("admin:auth_user_change", args=as_list(self.user.id)))
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

        self.inlines = self.response.context["inline_admin_formsets"]
        self.assertTrue(len(self.inlines) == 1)
        self.assertIs(self.inlines[0].opts.model, Staff)


class TestDocumentsAdmin(TestCase):
    response: HttpResponse
    inlines: Sequence[InlineModelAdmin]

    def setUp(self) -> None:
        super(TestDocumentsAdmin, self).setUp()
        self.user: User = self.create_user("staff", self.get_random_string(), is_superuser=True)
        self.staff: Staff = self.create_staff(self.user)
        self.client.force_login(self.user)
        self.lorem: File = ContentFile("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "lorem.txt")

    def test_get_inlines(self) -> None:
        self.response = self.client.get(reverse("admin:readable_documents_add"))
        self.inlines = self.response.context["inline_admin_formsets"]
        self.assertIsInstance(self.inlines, Sequence)
        self.assertTrue(len(self.inlines) == 0)

        document: Documents = Documents.objects.create(filename=self.lorem, uploaded_by=self.staff)
        self.response = self.client.get(reverse("admin:readable_documents_change", args=as_list(document.id)))
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
        self.assertEqual(cast(Documents, document).uploaded_by, self.staff)
