from django.urls.conf import path

from readable.api.views import document_list_create_view
from readable.api.views import document_retrieve_view
from readable.api.views import user_create_view
from readable.api.views import user_retrieve_update_view

# URL Dispatcher:

urlpatterns = [
    path("users/", user_create_view, name="api-user-create-view"),
    path("users/profile/", user_retrieve_update_view, name="api-user-retrieve-update-view"),
    path("documents/", document_list_create_view, name="api-document-list-create-view"),
    path("documents/<uuid:pk>/", document_retrieve_view, name="api-document-retrieve-view")
]
