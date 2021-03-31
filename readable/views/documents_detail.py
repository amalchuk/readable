from typing import Final

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as BaseModel
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.views.generic.detail import DetailView

from readable.models import Documents
from readable.types import ViewType

__all__: Final[list[str]] = ["documents_detail_view"]


class DocumentsDetailView(LoginRequiredMixin, DetailView):
    context_object_name: str = "document"
    http_method_names: list[str] = ["get"]
    model: type[BaseModel] = Documents
    template_name: str = "documents_detail.html"

    def get_queryset(self) -> "QuerySet[Documents]":
        return self.model.objects.filter(uploaded_by__user=self.request.user)


documents_detail_view: Final[ViewType] = DocumentsDetailView.as_view()
