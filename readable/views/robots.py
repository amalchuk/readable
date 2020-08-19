from typing import Any, Dict, Iterable, List

from django.http.response import HttpResponse
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView


class RobotsView(TemplateView):
    content_type = "text/plain"
    template_name = "robots.txt"

    @property
    def _robots(self) -> List[str]:
        return ["noindex", "noarchive"]

    @property
    def _allowed(self) -> List[str]:
        return ["index", "login", "registration"]

    @property
    def _disallowed(self) -> List[str]:
        return ["admin:index"]

    @property
    def _sitemaps(self) -> List[str]:
        return ["sitemap"]

    def _locations(self, urls: List[str]) -> List[str]:
        reversed_urls: Iterable[str] = map(reverse_lazy, urls)
        return list(map(self.request.build_absolute_uri, reversed_urls))

    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        response = super(RobotsView, self).dispatch(*args, **kwargs)
        response["X-Robots-Tag"] = ", ".join(self._robots)
        return response

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(RobotsView, self).get_context_data(**kwargs)
        context["allowed"] = self._locations(self._allowed)
        context["disallowed"] = self._locations(self._disallowed)
        context["sitemaps"] = self._locations(self._sitemaps)
        return context


robots_view = RobotsView.as_view()
