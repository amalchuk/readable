from decimal import Decimal

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from rest_framework.reverse import reverse

from readable.models import Documents
from readable.models import Metrics
from readable.models import Staff
from readable.public_api.serializers.documents import DocumentListSerializer
from readable.public_api.serializers.documents import MetricSerializer
from readable.utils.collections import as_list

from .utils import TestCase


class TestDocumentListSerializer(TestCase):
    def setUp(self) -> None:
        super(TestDocumentListSerializer, self).setUp()
        self.user: User = self.create_user("staff", self.get_random_string())
        self.staff: Staff = self.create_staff(self.user)
        self.lorem: ContentFile = ContentFile("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "lorem.txt")

    def test_nullable_get_metrics(self) -> None:
        document: Documents = Documents.objects.create(filename=self.lorem, uploaded_by=self.staff)
        serializer: DocumentListSerializer = DocumentListSerializer(document)
        self.assertIn("metrics", serializer.data)
        self.assertIsNone(serializer.data["metrics"])

    def test_get_metrics(self) -> None:
        document: Documents = Documents.objects.create(filename=self.lorem, status=Documents.Status.FINISHED, uploaded_by=self.staff)
        Metrics.objects.create(document=document)
        serializer: DocumentListSerializer = DocumentListSerializer(document)

        self.assertIn("metrics", serializer.data)
        self.assertIsNotNone(serializer.data["metrics"])

        expected_url: str = reverse("api-document-retrieve-view", args=as_list(document.id))
        self.assertEqual(serializer.data["metrics"], expected_url)


class TestMetricSerializer(TestCase):
    def setUp(self) -> None:
        super(TestMetricSerializer, self).setUp()
        self.user: User = self.create_user("staff", self.get_random_string())
        self.staff: Staff = self.create_staff(self.user)
        self.lorem: ContentFile = ContentFile("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "lorem.txt")

    def test_metrics(self) -> None:
        document: Documents = Documents.objects.create(filename=self.lorem, status=Documents.Status.FINISHED, uploaded_by=self.staff)
        metrics: Metrics = Metrics.objects.create(document=document, sentences=100, words=10000, letters=30000, syllables=2500)
        serializer: MetricSerializer = MetricSerializer(metrics)

        self.assertIn("flesch_reading_ease_score", serializer.data)
        self.assertIn("automated_readability_index", serializer.data)
        self.assertIn("coleman_liau_index", serializer.data)

        self.assertIsInstance(serializer.data["flesch_reading_ease_score"], float)
        self.assertIsInstance(serializer.data["automated_readability_index"], float)
        self.assertIsInstance(serializer.data["coleman_liau_index"], float)

        flesch_reading_ease_score: str = str(serializer.data["flesch_reading_ease_score"])
        automated_readability_index: str = str(serializer.data["automated_readability_index"])
        coleman_liau_index: str = str(serializer.data["coleman_liau_index"])

        self.assertLessEqual(abs(Decimal(flesch_reading_ease_score).as_tuple().exponent), 3)
        self.assertLessEqual(abs(Decimal(automated_readability_index).as_tuple().exponent), 3)
        self.assertLessEqual(abs(Decimal(coleman_liau_index).as_tuple().exponent), 3)
