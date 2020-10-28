from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic.detail import DetailView

from readable.models import Documents


class DocumentsDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "document"
    http_method_names = ["get"]
    model = Documents
    template_name = "documents_detail.html"

    def get_queryset(self) -> QuerySet:
        return self.model.objects.filter(uploaded_by__user=self.request.user)


documents_detail_view = DocumentsDetailView.as_view()
