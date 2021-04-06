"""
The ``typing`` module's aliases.
"""

from typing import Any, Final, Optional, Protocol

from django.http.request import HttpRequest
from django.http.response import HttpResponse

__all__: Final[list[str]] = ["FieldSetsType", "ViewType"]

FieldSetsType = list[tuple[Optional[str], dict[str, list[str]]]]


class ViewType(Protocol):
    def __call__(self, request: HttpRequest, /, *args: Any, **kwargs: Any) -> HttpResponse: ...
