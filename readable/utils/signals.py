from typing import Any

from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.utils.timezone import now
from scienco import compute_metrics
from simplethread import threaded

from readable.models import Documents
from readable.models import Metrics
from readable.models import Staff
from readable.utils.read_documents import read_document


@threaded
def file_processing(document: Documents) -> None:
    document.status = Documents.Status.IN_PROGRESS
    document.updated_at = now()
    document.save(update_fields=["status", "updated_at"])

    is_finished = False

    if text := read_document(document.path):
        metrics = compute_metrics(text)
        Metrics.objects.update_or_create(document=document, defaults={
            "is_russian": metrics.is_russian,
            "sentences": metrics.sentences,
            "words": metrics.words,
            "letters": metrics.letters,
            "syllables": metrics.syllables
        })
        is_finished = True

    document.status = Documents.Status.FINISHED if is_finished else Documents.Status.FAILED
    document.updated_at = now()
    document.save(update_fields=["status", "updated_at"])


def documents_uploaded(*args: Any, **kwargs: Any) -> None:
    is_created: bool = kwargs.pop("created")
    document: Documents = kwargs.pop("instance")

    if is_created and document.unavailable:
        file_processing(document)


def user_logged_in_out(*args: Any, **kwargs: Any) -> None:
    """
    Sent when the ``login`` and ``logout`` methods is called.
    """
    profile: User = kwargs.pop("user")
    request: HttpRequest = kwargs.pop("request")
    Staff.objects.update_or_create(user=profile, defaults={
        "user_agent": request.META.get("HTTP_USER_AGENT", None),
        "ip_address": request.META.get("REMOTE_ADDR", None)
    })
