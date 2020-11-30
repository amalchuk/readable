from typing import Any, Iterable
import xml.etree.ElementTree as etree

from django.conf import settings
from django.template.library import Library
from django.utils.encoding import force_str
from django.utils.encoding import smart_str
from django.utils.functional import keep_lazy_text
from django.utils.safestring import mark_safe

register = Library()


@keep_lazy_text
def create_meta(*, name: str, content: str, **kwargs: Any) -> str:
    element = etree.Element("meta", name=name, content=content, **kwargs)
    value = etree.tostring(element, encoding="unicode", method="html")
    return mark_safe(value)


@keep_lazy_text
def string_join(separator: str, iterable: Iterable[str]) -> str:
    return separator.join(map(force_str, iterable))


@register.simple_tag
def meta_description(*args: Any, **kwargs: Any) -> str:  # pragma: no cover
    # Exclude from the code coverage 'cause it's already covered in create_meta function.
    description = smart_str(settings.READABLE_META_DESCRIPTION)
    return create_meta(name="description", content=description)


@register.simple_tag
def meta_keywords(*args: Any, **kwargs: Any) -> str:  # pragma: no cover
    # Exclude from the code coverage 'cause it's already covered in create_meta function.
    keywords = string_join(", ", settings.READABLE_META_KEYWORDS)
    return create_meta(name="keywords", content=keywords)
