from typing import Final, Union

from django.contrib.admin.sites import site as default_site
from django.urls.conf import include
from django.urls.conf import path
from django.urls.resolvers import URLPattern
from django.utils.translation import gettext_lazy as _

from readable.public_api import urls as public_api
from readable.types import ViewType
from readable import views

__all__: Final[list[str]] = ["handler400", "handler403", "handler404", "handler500", "urlpatterns"]

# AdminSite settings:

default_site.site_title = default_site.site_header = _("readable")

default_site.index_title = _("Dashboard")

# URL Dispatcher:

urlpatterns: Final[list[URLPattern]] = [
    path("", views.index_view, name="index"),
    path("documents/<uuid:pk>/", views.documents_detail_view, name="documents-detail"),
    path("profile/login/", views.login_view, name="login"),
    path("profile/logout/", views.logout_view, name="logout"),
    path("profile/registration/", views.registration_view, name="registration"),
    path("profile/", views.profile_view, name="profile"),
    path("dashboard/", default_site.urls),
    path("api/", include(public_api))
]

# Override the built-in views:

handler400: Final[Union[str, ViewType]] = views.bad_request_view
handler403: Final[Union[str, ViewType]] = views.permission_denied_view
handler404: Final[Union[str, ViewType]] = views.page_not_found_view
handler500: Final[Union[str, ViewType]] = views.server_error_view
