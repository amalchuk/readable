"""
The ``typing`` module's aliases.
"""

from typing import Callable, Final, Optional

from django.http.response import HttpResponse

__all__: Final[list[str]] = ["FieldSetsType", "ViewType"]

FieldSetsType = list[tuple[Optional[str], dict[str, list[str]]]]
ViewType = Callable[..., HttpResponse]
