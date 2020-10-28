from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView

from readable.models import Documents


@method_decorator(login_required, name="get")
class DocumentsDetailView(DetailView):
    context_object_name = "document"
    http_method_names = ["get"]
    model = Documents
    template_name = "documents_detail.html"

    def get_queryset(self) -> QuerySet:
        return self.model.objects.filter(uploaded_by__user=self.request.user)


documents_detail_view = DocumentsDetailView.as_view()
