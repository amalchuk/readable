from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.core.files.base import ContentFile
from django.core.handlers.wsgi import WSGIRequest
from django.test.client import RequestFactory
from django.test.testcases import TestCase
from django.urls.base import reverse

from readable.models import Documents
from readable.models import Staff
from readable.utils.signals import file_processing

from .utils import TestCase as CommonTestCase
from .utils import create_user
from .utils import get_random_string


class TestDocumentsUploaded(CommonTestCase):
    def setUp(self) -> None:
        super(TestDocumentsUploaded, self).setUp()
        self.document: Documents

        self.user = self.create_user("staff", self.get_random_string())
        self.staff = self.create_staff(self.user)
        self.lorem = ContentFile("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "lorem.txt")
        self.empty = ContentFile("", "empty.txt")

    def test_file_processing(self) -> None:
        self.document = Documents.objects.create(filename=self.lorem, uploaded_by=self.staff)
        file_processing(self.document)
        self.assertEqual(self.document.status, Documents.Status.FINISHED)
        self.assertTrue(hasattr(self.document, "metrics"))
        self.assertFalse(self.document.metrics.is_russian)

        self.document = Documents.objects.create(filename=self.empty, uploaded_by=self.staff)
        file_processing(self.document)
        self.assertEqual(self.document.status, Documents.Status.FINISHED)
        self.assertFalse(hasattr(self.document, "metrics"))


class TestUserLoggedInOut(TestCase):
    def setUp(self) -> None:
        self.username = "staff"
        self.password = get_random_string()
        self.user = create_user(self.username, self.password)
        self.factory = RequestFactory()

    def test_login(self) -> None:
        defaults: dict[str, str] = {
            "HTTP_USER_AGENT": "Mozilla/5.0 TestCase/Login",
            "REMOTE_ADDR": "127.0.0.1"
        }
        request: WSGIRequest = self.factory.post(reverse("admin:login"), data={
            "username": self.username,
            "password": self.password
        }, **defaults)
        sender: type[User] = getattr(self.user, "__class__")

        user_logged_in.send(sender=sender, request=request, user=self.user)
        self.assertTrue(Staff.objects.filter(user=self.user).exists())

        staff: Staff = Staff.objects.get(user=self.user)
        self.assertEqual(staff.user_agent, defaults["HTTP_USER_AGENT"])
        self.assertEqual(staff.ip_address, defaults["REMOTE_ADDR"])

    def test_logout(self) -> None:
        defaults: dict[str, str] = {
            "HTTP_USER_AGENT": "Mozilla/5.0 TestCase/Logout",
            "REMOTE_ADDR": "Unsupported IP address"
        }
        request: WSGIRequest = self.factory.post(reverse("admin:logout"), **defaults)
        request.user = self.user
        sender: type[User] = getattr(self.user, "__class__")

        user_logged_out.send(sender=sender, request=request, user=self.user)
        self.assertTrue(Staff.objects.filter(user=self.user).exists())

        staff: Staff = Staff.objects.get(user=self.user)
        self.assertEqual(staff.user_agent, defaults["HTTP_USER_AGENT"])
        self.assertIsNone(staff.ip_address)


class TestUserStaffIsCreated(TestCase):
    def setUp(self) -> None:
        self.username = "staff"
        self.password = get_random_string()

    def test_user_staff_is_created(self) -> None:
        self.assertEqual(Staff.objects.count(), 0)
        user: User = create_user(self.username, self.password)
        self.assertTrue(Staff.objects.filter(user=user).exists())
