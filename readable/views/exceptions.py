from typing import Any, Final, Union

from django.http.response import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponseNotFound
from django.http.response import HttpResponseServerError
from django.template.loader import render_to_string as _

from readable.types import ViewType

__all__: Final[list[str]] = ["bad_request_view", "page_not_found_view", "permission_denied_view", "server_error_view"]


def exception_handler(template_name: Union[list[str], str], response: type[HttpResponse], /, **context: Any) -> ViewType:
    context.setdefault("status_code", response.status_code)
    return lambda request, *args, **kwargs: response(_(template_name, context=context, request=request))


bad_request_view: Final[ViewType] = exception_handler("exceptions_bad_request.html", HttpResponseBadRequest)
permission_denied_view: Final[ViewType] = exception_handler("exceptions_permission_denied.html", HttpResponseForbidden)
page_not_found_view: Final[ViewType] = exception_handler("exceptions_page_not_found.html", HttpResponseNotFound)
server_error_view: Final[ViewType] = exception_handler("exceptions_server_error.html", HttpResponseServerError)
