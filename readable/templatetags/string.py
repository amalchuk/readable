from os import linesep as separator
from typing import Iterable

from django.template.library import Library
from django.utils.encoding import smart_str

register = Library()


@register.filter(is_safe=True)
def line_breaks(iterable: Iterable[str], prefix: str) -> str:
    add_prefix = lambda item: f"{prefix}{item}"
    return separator.join(map(add_prefix, map(smart_str, iterable)))
