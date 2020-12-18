from typing import Callable, List, Union

from django.contrib.admin.sites import site as default_site
from django.http.response import HttpResponse
from django.urls.conf import include
from django.urls.conf import path
from django.urls.resolvers import URLPattern
from django.utils.translation import gettext_lazy as _

import readable.views as views

__all__: List[str] = ["handler400", "handler403", "handler404", "handler500", "urlpatterns"]

# AdminSite settings:

default_site.site_title = default_site.site_header = _("readable")

default_site.index_title = _("Dashboard")

# URL Dispatcher:

urlpatterns: List[URLPattern] = [
    path("", views.index_view, name="index"),
    path("documents/<uuid:pk>/", views.documents_detail_view, name="documents-detail"),
    path("profile/login/", views.login_view, name="login"),
    path("profile/logout/", views.logout_view, name="logout"),
    path("profile/registration/", views.registration_view, name="registration"),
    path("profile/", views.profile_view, name="profile"),
    path("dashboard/", default_site.urls),
    path("api/", include("readable.public_api.urls"))
]

# Override the built-in views:

handler400: Union[str, Callable[..., HttpResponse]] = views.bad_request_view
handler403: Union[str, Callable[..., HttpResponse]] = views.permission_denied_view
handler404: Union[str, Callable[..., HttpResponse]] = views.page_not_found_view
handler500: Union[str, Callable[..., HttpResponse]] = views.server_error_view
