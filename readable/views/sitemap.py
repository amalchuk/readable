from typing import Any, Dict, Iterable, List

from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from readable.utils.decorators import x_robots_tag


@method_decorator(x_robots_tag, name="dispatch")
class SitemapView(TemplateView):
    content_type = "application/xml"
    template_name = "sitemap.xml"

    @property
    def _urls(self) -> List[str]:
        return ["index", "login", "registration"]

    def _locations(self, urls: List[str]) -> List[str]:
        reversed_urls: Iterable[str] = map(reverse_lazy, urls)
        return list(map(self.request.build_absolute_uri, reversed_urls))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(SitemapView, self).get_context_data(**kwargs)
        context["locations"] = self._locations(self._urls)
        return context


sitemap_view = SitemapView.as_view()
