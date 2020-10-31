from typing import Any, Dict

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import HttpResponse
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView

from readable.forms import DocumentsForm
from readable.models import Documents


@method_decorator(login_required, name="post")
class IndexView(CreateView):
    form_class = DocumentsForm
    http_method_names = ["get", "post"]
    success_url = reverse_lazy("index")
    template_name = "index.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        if self.request.user.is_authenticated:
            documents = Documents.objects.filter(uploaded_by__user=self.request.user)
            paginator = Paginator(documents, settings.READABLE_DOCUMENTS_PAGINATE_BY)

            page = self.request.GET.get("page")
            kwargs["documents"] = paginator.get_page(page)
        return super(IndexView, self).get_context_data(**kwargs)

    def form_valid(self, form: DocumentsForm) -> HttpResponse:
        form.instance.uploaded_by = self.request.user.staff
        return super(IndexView, self).form_valid(form)


index_view = IndexView.as_view()
