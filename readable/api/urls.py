from django.urls.conf import path

from readable.api.views import document_create_view
from readable.api.views import user_create_view
from readable.api.views import user_retrieve_update_view

# URL Dispatcher:

urlpatterns = [
    path("users/", user_create_view, name="api-user-create-view"),
    path("users/profile/", user_retrieve_update_view, name="api-user-retrieve-update-view"),
    path("documents/", document_create_view, name="api-document-create-view")
]
