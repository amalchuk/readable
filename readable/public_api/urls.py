from typing import Final

from django.urls.conf import path
from django.urls.resolvers import URLPattern

import readable.public_api.views as views

__all__: Final[list[str]] = ["urlpatterns"]

# URL Dispatcher:

urlpatterns: Final[list[URLPattern]] = [
    path("users/", views.user_create_view, name="api-user-create-view"),
    path("users/profile/", views.user_retrieve_update_view, name="api-user-retrieve-update-view"),
    path("documents/", views.document_list_create_view, name="api-document-list-create-view"),
    path("documents/<uuid:pk>/", views.document_retrieve_view, name="api-document-retrieve-view")
]
