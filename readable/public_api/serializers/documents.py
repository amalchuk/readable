from typing import Final, List, Type

from django.db.models.base import Model as BaseModel
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import BooleanField
from rest_framework.fields import CharField
from rest_framework.fields import FileField
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from readable.models import Documents
from readable.models import Metrics
from readable.utils.collections import as_list
from readable.utils.validators import validate_filename

__all__: Final[List[str]] = [
    "DocumentCreateSerializer",
    "DocumentListSerializer",
    "DocumentRetrieveSerializer",
    "MetricSerializer"
]


class DocumentCreateSerializer(ModelSerializer):
    filename = FileField(label=_("Document"), write_only=True, validators=as_list(validate_filename))

    class Meta:
        model: Type[BaseModel] = Documents
        fields: List[str] = ["id", "filename"]


class DocumentListSerializer(ModelSerializer):
    filename = CharField(label=_("Document"), source="realname")
    is_unavailable = BooleanField(read_only=True, source="unavailable")
    status = CharField(label=_("Status"), source="get_status_display")

    class Meta:
        model: Type[BaseModel] = Documents
        fields: List[str] = ["id", "filename", "is_unavailable", "status", "created_at", "updated_at"]


class MetricSerializer(ModelSerializer):
    flesch_reading_ease_score = SerializerMethodField(label=_("Flesch-Kincaid score"))
    automated_readability_index = SerializerMethodField(label=_("Automated readability index"))
    coleman_liau_index = SerializerMethodField(label=_("Coleman-Liau index"))

    class Meta:
        model: Type[BaseModel] = Metrics
        fields: List[str] = [
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

    class Meta:
        model: Type[BaseModel] = Documents
        fields: List[str] = ["id", "filename", "status", "metrics", "created_at", "updated_at"]
