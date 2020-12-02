from django.utils.translation import gettext_lazy as _
from rest_framework.fields import FileField
from rest_framework.serializers import ModelSerializer

from readable.models import Documents
from readable.utils.validators import validate_filename as is_supported_extension

__all__ = ["DocumentCreateSerializer"]


class DocumentCreateSerializer(ModelSerializer):
    filename = FileField(label=_("Document"), write_only=True, validators=[is_supported_extension])

    class Meta:
        model = Documents
        fields = ["id", "filename"]
