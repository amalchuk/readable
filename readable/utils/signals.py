from ipaddress import IPv4Address
from ipaddress import IPv6Address
from ipaddress import ip_address as parse_ip
from typing import Any, Final, Optional, Union

from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.utils.timezone import now
from scienco import Metrics as ComputedMetrics
from scienco import compute_metrics
from simplethread import synchronized
from simplethread import threaded

from readable.models import Documents
from readable.models import Metrics
from readable.models import Staff
from readable.utils.collections import as_list
from readable.utils.read_documents import read_document

from _thread import get_ident

__all__: Final[list[str]] = ["documents_uploaded", "user_logged_in_out", "user_staff_is_created"]


@synchronized
def file_processing(document: Documents, *, thread_identifier: Optional[int] = None) -> None:
    update_fields: list[str] = as_list("status", "updated_at")

    document.status = Documents.Status.IN_PROGRESS
    document.updated_at = now()
    document.save(update_fields=update_fields)

    if text := read_document(document.path):
        metrics: ComputedMetrics = compute_metrics(text)
        Metrics.objects.update_or_create(document=document, defaults={
            "is_russian": metrics.is_russian,
            "sentences": metrics.sentences,
            "words": metrics.words,
            "letters": metrics.letters,
            "syllables": metrics.syllables
        })

    document.status = Documents.Status.FAILED if text is None else Documents.Status.FINISHED
    document.updated_at = now()
    document.save(update_fields=update_fields)

    if thread_identifier is not None and thread_identifier != get_ident():  # pragma: no cover
        # Exit from the interpreter immediately:
        raise SystemExit from None


def documents_uploaded(*args: Any, **kwargs: Any) -> None:  # pragma: no cover
    # Exclude from the code coverage 'cause it's called in another thread without additional conditions.
    is_created: bool = kwargs.pop("created")
    document: Documents = kwargs.pop("instance")

    if is_created and document.unavailable:
        running_in_background = threaded(file_processing)
        running_in_background(document, thread_identifier=get_ident())


def user_logged_in_out(*args: Any, **kwargs: Any) -> None:
    """
    Sent when the ``login`` and ``logout`` methods is called.
    """
    profile: User = kwargs.pop("user")
    request: HttpRequest = kwargs.pop("request")

    user_agent: Optional[str] = request.META.get("HTTP_USER_AGENT", None)
    ip_address: Optional[str] = request.META.get("HTTP_X_REAL_IP", request.META.get("REMOTE_ADDR", None))

    try:
        raw_address: Union[IPv4Address, IPv6Address] = parse_ip(ip_address)
    except ValueError:
        ip_address = None
    else:
        ip_address = str(raw_address)

    Staff.objects.update_or_create(user=profile, defaults={
        "user_agent": user_agent,
        "ip_address": ip_address
    })


def user_staff_is_created(*args: Any, **kwargs: Any) -> None:
    """
    Ensure that the ``Staff`` object has been created.
    """
    is_created: bool = kwargs.pop("created")
    profile: User = kwargs.pop("instance")

    if is_created and not Staff.objects.filter(user=profile).exists():
        Staff.objects.create(user=profile)
