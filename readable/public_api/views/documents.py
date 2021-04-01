from typing import Final, Literal, cast

from django.db.models.query import QuerySet
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import BaseParser
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.serializers import BaseSerializer

from readable.models import Documents
from readable.models import Staff
from readable.public_api.serializers.documents import DocumentCreateSerializer
from readable.public_api.serializers.documents import DocumentListSerializer
from readable.public_api.serializers.documents import DocumentRetrieveSerializer
from readable.types import ViewType
from readable.utils.collections import as_list

__all__: Final[list[str]] = ["document_list_create_view", "document_retrieve_view"]

_R = Literal["get", "post"]


class DocumentListCreateAPIView(ListCreateAPIView):
    parser_method_classes: dict[str, type[BaseParser]] = {
        "get": JSONParser,
        "post": MultiPartParser
    }
    serializer_method_classes: dict[str, type[BaseSerializer]] = {
        "get": DocumentListSerializer,
        "post": DocumentCreateSerializer
    }

    @property
    def request_method(self) -> _R:
        return cast(_R, (self.request.method or "GET").lower())

    def get_parsers(self) -> list[BaseParser]:
        parser_type: type[BaseParser] = self.parser_method_classes[self.request_method]
        parser: BaseParser = parser_type()
        return as_list(parser)

    def get_serializer_class(self) -> type[BaseSerializer]:
        return self.serializer_method_classes[self.request_method]

    def get_queryset(self) -> "QuerySet[Documents]":
        return Documents.objects.filter(uploaded_by__user=self.request.user)

    def perform_create(self, serializer: DocumentCreateSerializer) -> None:
        uploaded_by: Staff = self.request.user.staff
        serializer.save(uploaded_by=uploaded_by)


class DocumentRetrieveAPIView(RetrieveAPIView):
    serializer_class: type[BaseSerializer] = DocumentRetrieveSerializer

    def get_queryset(self) -> "QuerySet[Documents]":
        return Documents.objects.filter(uploaded_by__user=self.request.user)


document_list_create_view: Final[ViewType] = DocumentListCreateAPIView.as_view()
document_retrieve_view: Final[ViewType] = DocumentRetrieveAPIView.as_view()
