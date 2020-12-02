from django.contrib.admin.sites import site as default_site
from django.urls.conf import include
from django.urls.conf import path
from django.utils.translation import gettext_lazy as _

from readable.views.authorization import login_view
from readable.views.authorization import logout_view
from readable.views.authorization import registration_view
from readable.views.documents_detail import documents_detail_view
from readable.views.index import index_view
from readable.views.profile import profile_view

# AdminSite settings:

default_site.site_title = default_site.site_header = _("readable")

default_site.index_title = _("Dashboard")

# URL Dispatcher:

urlpatterns = [
    path("", index_view, name="index"),
    path("documents/<uuid:pk>/", documents_detail_view, name="documents_detail"),
    path("profile/login/", login_view, name="login"),
    path("profile/logout/", logout_view, name="logout"),
    path("profile/registration/", registration_view, name="registration"),
    path("profile/", profile_view, name="profile"),
    path("dashboard/", default_site.urls),
    path("api/", include("readable.api.urls"))
]
