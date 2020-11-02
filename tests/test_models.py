from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.test.testcases import TestCase

from readable.models import Documents
from readable.models import Staff
from readable.utils.signals import documents_uploaded


class TestDocuments(TestCase):
    def setUp(self) -> None:
        self.lorem: ContentFile = ContentFile("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "lorem.txt")
        self.user: User = User.objects.create_user(username="staff", password="staff")
        self.staff: Staff = Staff.objects.create(user=self.user)

    def test_upload_directory(self) -> None:
        # Temporarily disable the "documents_uploaded" signal:
        post_save.disconnect(documents_uploaded, Documents)

        document: Documents = Documents.objects.create(filename=self.lorem, uploaded_by=self.staff)
        self.assertEqual(document.realname, self.lorem.name)
        self.assertEqual(document.filename, f"{document.id!s}{document.path.suffix}")

        self.assertTrue(document.unavailable)
        document.status = Documents.Status.FINISHED
        document.save(update_fields=["status"])
        self.assertFalse(document.unavailable)
