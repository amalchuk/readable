from django.core.files.base import ContentFile

from readable.models import Documents
from tests.common import TestCase


class TestDocuments(TestCase):
    def setUp(self) -> None:
        super(TestDocuments, self).setUp()
        self.user, self.staff = self.create_user(username="staff", password=self.get_random_string())
        self.lorem = ContentFile("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "lorem.txt")

    def test_upload_directory(self) -> None:
        document: Documents = Documents.objects.create(filename=self.lorem, uploaded_by=self.staff)
        self.assertEqual(document.realname, self.lorem.name)
        self.assertEqual(document.filename, f"{document.id!s}{document.path.suffix}")

        self.assertTrue(document.unavailable)
        document.status = Documents.Status.FINISHED
        document.save(update_fields=["status"])
        self.assertFalse(document.unavailable)
