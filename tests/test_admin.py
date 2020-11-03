from http import HTTPStatus
from typing import Sequence

from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.test.testcases import TestCase
from django.urls.base import reverse

from readable.models import Staff


class TestUserAdmin(TestCase):
    def setUp(self) -> None:
        self.response: HttpResponse
        self.inlines: Sequence[InlineModelAdmin]

        self.user: User = User.objects.create_superuser(username="staff", password="staff")
        self.staff: Staff = Staff.objects.create(user=self.user)
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
