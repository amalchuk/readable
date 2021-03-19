from typing import Final, Optional

from django.db.models.base import Model as BaseModel
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CharField
from rest_framework.fields import FileField
from rest_framework.fields import SerializerMethodField
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer

from readable.models import Documents
from readable.models import Metrics
from readable.utils.collections import as_list
from readable.utils.validators import validate_filename

__all__: Final[list[str]] = [
    "DocumentCreateSerializer",
    "DocumentListSerializer",
    "DocumentRetrieveSerializer",
    "MetricSerializer"
]


class DocumentCreateSerializer(ModelSerializer):
    filename = FileField(label=_("Document"), write_only=True, validators=as_list(validate_filename))

    class Meta:
        model: type[BaseModel] = Documents
        fields: list[str] = ["id", "filename"]


class DocumentListSerializer(ModelSerializer):
    filename = CharField(label=_("Document"), source="realname")
    status = CharField(label=_("Status"), source="get_status_display")
    metrics = SerializerMethodField(label=_("Metrics"))

    class Meta:
        model: type[BaseModel] = Documents
        fields: list[str] = ["id", "filename", "status", "metrics", "created_at", "updated_at"]

    def get_metrics(self, obj: Documents, /) -> Optional[str]:
        request: Optional[Request] = self.context.get("request")
        return reverse("api-document-retrieve-view", args=as_list(obj.id), request=request) if not obj.unavailable else None


class MetricSerializer(ModelSerializer):
    flesch_reading_ease_score = SerializerMethodField(label=_("Flesch-Kincaid score"))
    automated_readability_index = SerializerMethodField(label=_("Automated readability index"))
    coleman_liau_index = SerializerMethodField(label=_("Coleman-Liau index"))

    class Meta:
        model: type[BaseModel] = Metrics
        fields: list[str] = [
            "is_russian",
            "sentences",
            "words",
            "letters",
            "syllables",
            "flesch_reading_ease_score",
            "automated_readability_index",
            "coleman_liau_index"
        ]

    def get_flesch_reading_ease_score(self, obj: Metrics, /) -> float:
        return round(obj.indexes.flesch_reading_ease_score, 0b110)

    def get_automated_readability_index(self, obj: Metrics, /) -> float:
        return round(obj.indexes.automated_readability_index, 0b110)

    def get_coleman_liau_index(self, obj: Metrics, /) -> float:
        return round(obj.indexes.coleman_liau_index, 0b110)


class DocumentRetrieveSerializer(DocumentListSerializer):
    metrics = MetricSerializer(label=_("Metrics"), read_only=True)
