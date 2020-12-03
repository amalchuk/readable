from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CharField
from rest_framework.fields import FileField
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from readable.models import Documents
from readable.models import Metrics
from readable.utils.validators import validate_filename as is_supported_extension

__all__ = ["DocumentCreateSerializer", "DocumentListSerializer", "DocumentRetrieveSerializer", "MetricsSerializer"]


class DocumentCreateSerializer(ModelSerializer):
    filename = FileField(label=_("Document"), write_only=True, validators=[is_supported_extension])

    class Meta:
        model = Documents
        fields = ["id", "filename"]


class DocumentListSerializer(ModelSerializer):
    filename = CharField(label=_("Document"), source="realname")
    status = CharField(label=_("Status"), source="get_status_display")

    class Meta:
        model = Documents
        fields = ["id", "filename", "status", "created_at", "updated_at"]


class MetricsSerializer(ModelSerializer):
    flesch_reading_ease_score = SerializerMethodField(label=_("Flesch-Kincaid score"))
    automated_readability_index = SerializerMethodField(label=_("Automated readability index"))
    coleman_liau_index = SerializerMethodField(label=_("Coleman-Liau index"))

    class Meta:
        model = Metrics
        fields = [
            "is_russian",
            "sentences",
            "words",
            "letters",
            "syllables",
            "flesch_reading_ease_score",
            "automated_readability_index",
            "coleman_liau_index"
        ]

    def get_flesch_reading_ease_score(self, obj: Metrics) -> float:
        return obj.indexes.flesch_reading_ease_score

    def get_automated_readability_index(self, obj: Metrics) -> float:
        return obj.indexes.automated_readability_index

    def get_coleman_liau_index(self, obj: Metrics) -> float:
        return obj.indexes.coleman_liau_index


class DocumentRetrieveSerializer(DocumentListSerializer):
    metrics = MetricsSerializer(label=_("Metrics"), read_only=True)

    class Meta:
        model = Documents
        fields = ["id", "filename", "status", "metrics", "created_at", "updated_at"]
