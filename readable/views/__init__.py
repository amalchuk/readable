from typing import Final

from readable.views.authorization import login_view
from readable.views.authorization import logout_view
from readable.views.authorization import registration_view
from readable.views.documents_detail import documents_detail_view
from readable.views.exceptions import bad_request_view
from readable.views.exceptions import forbidden_view
from readable.views.exceptions import internal_server_error_view
from readable.views.exceptions import not_found_view
from readable.views.index import index_view
from readable.views.profile import profile_view

__all__: Final[list[str]] = [
    "login_view",
    "logout_view",
    "registration_view",
    "documents_detail_view",
    "bad_request_view",
    "forbidden_view",
    "internal_server_error_view",
    "not_found_view",
    "index_view",
    "profile_view"
]
