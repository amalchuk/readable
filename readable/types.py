"""
The ``typing`` module's aliases.
"""

from typing import Callable, Final, Mapping, Optional, Sequence

from django.http.response import HttpResponse

__all__: Final[list[str]] = ["FieldSetsType", "ViewType"]

FieldSetsType = Sequence[tuple[Optional[str], Mapping[str, Sequence[str]]]]
ViewType = Callable[..., HttpResponse]
