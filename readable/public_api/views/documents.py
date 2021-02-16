from typing import Callable, Dict, Final, List, Literal, Type

from django.db.models.query import QuerySet
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import BaseParser
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from readable.models import Documents
from readable.models import Staff
from readable.public_api.serializers.documents import DocumentCreateSerializer
from readable.public_api.serializers.documents import DocumentListSerializer
from readable.public_api.serializers.documents import DocumentRetrieveSerializer
from readable.utils.collections import as_list

__all__: Final[List[str]] = ["document_list_create_view", "document_retrieve_view"]


class DocumentListCreateAPIView(ListCreateAPIView):
    parser_method_classes: Dict[str, Type[BaseParser]] = {
        "get": JSONParser,
        "post": MultiPartParser
    }
    serializer_method_classes: Dict[str, Type[BaseSerializer]] = {
        "get": DocumentListSerializer,
        "post": DocumentCreateSerializer
    }

    @property
    def request_method(self) -> Literal["get", "post"]:
        return self.request.method.lower()

    def get_parsers(self) -> List[BaseParser]:
        parser_type: Type[BaseParser] = self.parser_method_classes[self.request_method]
        parser: BaseParser = parser_type()
        return as_list(parser)

    def get_serializer_class(self) -> Type[BaseSerializer]:
        return self.serializer_method_classes[self.request_method]

    def get_queryset(self) -> "QuerySet[Documents]":
        return Documents.objects.filter(uploaded_by__user=self.request.user)

    def perform_create(self, serializer: DocumentCreateSerializer) -> None:
        uploaded_by: Staff = self.request.user.staff
        serializer.save(uploaded_by=uploaded_by)


class DocumentRetrieveAPIView(RetrieveAPIView):
    serializer_class: Type[BaseSerializer] = DocumentRetrieveSerializer

    def get_queryset(self) -> "QuerySet[Documents]":
        return Documents.objects.filter(uploaded_by__user=self.request.user)


document_list_create_view: Callable[..., Response] = DocumentListCreateAPIView.as_view()
document_retrieve_view: Callable[..., Response] = DocumentRetrieveAPIView.as_view()
