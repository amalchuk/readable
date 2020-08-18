from typing import Any, Dict, Iterable, List

from django.http.response import HttpResponse
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView


class SitemapView(TemplateView):
    content_type = "application/xml"
    template_name = "sitemap.xml"

    @property
    def robots(self) -> List[str]:
        return ["noindex", "noarchive"]

    @property
    def urls(self) -> List[str]:
        return ["index", "login", "registration"]

    @property
    def locations(self) -> List[str]:
        urls: Iterable[str] = map(reverse_lazy, self.urls)
        return list(map(self.request.build_absolute_uri, urls))

    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        response = super(SitemapView, self).dispatch(*args, **kwargs)
        response["X-Robots-Tag"] = ", ".join(self.robots)
        return response

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(SitemapView, self).get_context_data(**kwargs)
        context["locations"] = self.locations
        return context


sitemap_view = SitemapView.as_view()
