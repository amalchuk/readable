from http import HTTPStatus
from typing import Any, Final, Sequence, Union

from django.shortcuts import render
from django.views.decorators.cache import never_cache

from readable.types import ViewType

__all__: Final[list[str]] = ["bad_request_view", "forbidden_view", "internal_server_error_view", "not_found_view"]


def _(template_name: Union[str, Sequence[str]], status_code: int, /, **context: Any) -> ViewType:
    context.setdefault("status_code", status_code)
    handler: ViewType = lambda request, *args, **kwargs: render(request, template_name, context, status=status_code)
    return never_cache(handler)


bad_request_view: Final[ViewType] = _("exceptions_bad_request.html", HTTPStatus.BAD_REQUEST)
forbidden_view: Final[ViewType] = _("exceptions_permission_denied.html", HTTPStatus.FORBIDDEN)
not_found_view: Final[ViewType] = _("exceptions_page_not_found.html", HTTPStatus.NOT_FOUND)
internal_server_error_view: Final[ViewType] = _("exceptions_server_error.html", HTTPStatus.INTERNAL_SERVER_ERROR)
