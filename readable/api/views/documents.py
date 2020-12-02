from typing import Dict, Type

from django.db.models.query import QuerySet
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.serializers import BaseSerializer

from readable.api.serializers.documents import DocumentCreateSerializer
from readable.api.serializers.documents import DocumentListSerializer
from readable.api.serializers.documents import DocumentRetrieveSerializer
from readable.models import Documents
from readable.models import Staff

__all__ = ["document_list_create_view", "document_retrieve_view"]


class DocumentListCreateAPIView(ListCreateAPIView):
    serializer_method_classes: Dict[str, Type[BaseSerializer]] = {
        "get": DocumentListSerializer,
        "post": DocumentCreateSerializer
    }

    def get_serializer_class(self) -> Type[BaseSerializer]:
        request_method: str = self.request.method.lower()
        return self.serializer_method_classes[request_method]

    def get_queryset(self) -> "QuerySet[Documents]":
        return Documents.objects.filter(uploaded_by__user=self.request.user)

    def perform_create(self, serializer: DocumentCreateSerializer) -> None:
        uploaded_by: Staff = self.request.user.staff
        serializer.save(uploaded_by=uploaded_by)


class DocumentRetrieveAPIView(RetrieveAPIView):
    serializer_class = DocumentRetrieveSerializer

    def get_queryset(self) -> "QuerySet[Documents]":
        return Documents.objects.filter(uploaded_by__user=self.request.user)


document_list_create_view = DocumentListCreateAPIView.as_view()
document_retrieve_view = DocumentRetrieveAPIView.as_view()
