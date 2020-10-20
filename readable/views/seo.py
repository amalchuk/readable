from typing import Any, Dict, Iterable, List

from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from readable.utils.decorators import x_robots_tag


@method_decorator(x_robots_tag, name="dispatch")
class RobotsView(TemplateView):
    content_type = "text/plain"
    template_name = "seo/robots.txt"

    @property
    def _allowed(self) -> List[str]:
        return ["index", "login", "registration"]

    @property
    def _disallowed(self) -> List[str]:
        return ["admin:index", "admin:login", "admin:logout"]

    @property
    def _sitemap(self) -> str:
        sitemap_location: str = reverse_lazy("sitemap")
        return self.request.build_absolute_uri(sitemap_location)

    def _locations(self, urls: List[str]) -> List[str]:
        return list(map(reverse_lazy, urls))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(RobotsView, self).get_context_data(**kwargs)
        context["allowed"] = self._locations(self._allowed)
        context["disallowed"] = self._locations(self._disallowed)
        context["sitemap"] = self._sitemap
        return context


@method_decorator(x_robots_tag, name="dispatch")
class SitemapView(TemplateView):
    content_type = "application/xml"
    template_name = "seo/sitemap.xml"

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


robots_view = RobotsView.as_view()
sitemap_view = SitemapView.as_view()