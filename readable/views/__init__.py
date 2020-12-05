from readable.views.authorization import login_view
from readable.views.authorization import logout_view
from readable.views.authorization import registration_view
from readable.views.documents_detail import documents_detail_view
from readable.views.exceptions import bad_request_view
from readable.views.exceptions import page_not_found_view
from readable.views.exceptions import permission_denied_view
from readable.views.exceptions import server_error_view
from readable.views.index import index_view
from readable.views.profile import profile_view

__all__ = [
    "login_view",
    "logout_view",
    "registration_view",
    "documents_detail_view",
    "bad_request_view",
    "page_not_found_view",
    "permission_denied_view",
    "server_error_view",
    "index_view",
    "profile_view"
]
