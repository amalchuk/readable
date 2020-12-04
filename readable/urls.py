from django.contrib.admin.sites import site as default_site
from django.urls.conf import include
from django.urls.conf import path
from django.utils.translation import gettext_lazy as _

import readable.views as views

# AdminSite settings:

default_site.site_title = default_site.site_header = _("readable")

default_site.index_title = _("Dashboard")

# URL Dispatcher:

urlpatterns = [
    path("", views.index_view, name="index"),
    path("documents/<uuid:pk>/", views.documents_detail_view, name="documents-detail"),
    path("profile/login/", views.login_view, name="login"),
    path("profile/logout/", views.logout_view, name="logout"),
    path("profile/registration/", views.registration_view, name="registration"),
    path("profile/", views.profile_view, name="profile"),
    path("dashboard/", default_site.urls),
    path("api/", include("readable.public_api.urls"))
]
