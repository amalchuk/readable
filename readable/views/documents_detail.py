from typing import Callable, Final, List, Type

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as BaseModel
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.views.generic.detail import DetailView

from readable.models import Documents

__all__: Final[List[str]] = ["documents_detail_view"]


class DocumentsDetailView(LoginRequiredMixin, DetailView):
    context_object_name: str = "document"
    http_method_names: List[str] = ["get"]
    model: Type[BaseModel] = Documents
    template_name: str = "documents_detail.html"

    def get_queryset(self) -> "QuerySet[Documents]":
        return self.model.objects.filter(uploaded_by__user=self.request.user)


documents_detail_view: Callable[..., HttpResponse] = DocumentsDetailView.as_view()
