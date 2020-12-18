from typing import Any, List, Type

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponseNotFound
from django.http.response import HttpResponseServerError
from django.template.loader import render_to_string as _

__all__: List[str] = ["bad_request_view", "page_not_found_view", "permission_denied_view", "server_error_view"]


def bad_request_view(request: HttpRequest, *args: Any, **context: Any) -> HttpResponse:
    response: Type[HttpResponse] = HttpResponseBadRequest
    context.setdefault("status_code", response.status_code)
    return response(_("exceptions_bad_request.html", context=context, request=request))


def permission_denied_view(request: HttpRequest, *args: Any, **context: Any) -> HttpResponse:
    response: Type[HttpResponse] = HttpResponseForbidden
    context.setdefault("status_code", response.status_code)
    return response(_("exceptions_permission_denied.html", context=context, request=request))


def page_not_found_view(request: HttpRequest, *args: Any, **context: Any) -> HttpResponse:
    response: Type[HttpResponse] = HttpResponseNotFound
    context.setdefault("status_code", response.status_code)
    return response(_("exceptions_page_not_found.html", context=context, request=request))


def server_error_view(request: HttpRequest, *args: Any, **context: Any) -> HttpResponse:
    response: Type[HttpResponse] = HttpResponseServerError
    context.setdefault("status_code", response.status_code)
    return response(_("exceptions_server_error.html", context=context, request=request))
