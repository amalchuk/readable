from typing import Any, Dict, Iterable, List

from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from readable.utils.decorators import x_robots_tag


@method_decorator(x_robots_tag, name="dispatch")
class RobotsView(TemplateView):
    content_type = "text/plain"
    template_name = "robots.txt"

    @property
    def _disallowed(self) -> List[str]:
        return ["admin:index", "admin:login", "admin:logout"]

    @property
    def _sitemaps(self) -> List[str]:
        return ["sitemap"]

    def _locations(self, urls: List[str]) -> List[str]:
        reversed_urls: Iterable[str] = map(reverse_lazy, urls)
        return list(map(self.request.build_absolute_uri, reversed_urls))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(RobotsView, self).get_context_data(**kwargs)
        context["disallowed"] = self._locations(self._disallowed)
        context["sitemaps"] = self._locations(self._sitemaps)
        return context


robots_view = RobotsView.as_view()
