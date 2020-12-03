from typing import Any

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
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


@receiver(post_save, sender=Documents)
def documents_uploaded(*args: Any, **kwargs: Any) -> None:  # pragma: no cover
    # Exclude from the code coverage 'cause it's called in another thread without additional conditions.
    is_created: bool = kwargs.pop("created")
    document: Documents = kwargs.pop("instance")

    if is_created and document.unavailable:
        file_processing(document)


@receiver([user_logged_in, user_logged_out])
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


@receiver(post_save, sender=User)
def user_staff_is_created(*args: Any, **kwargs: Any) -> None:
    """
    Ensure that the ``Staff`` object has been created.
    """
    is_created: bool = kwargs.pop("created")
    profile: User = kwargs.pop("instance")

    if is_created and not Staff.objects.filter(user=profile).exists():
        Staff.objects.create(user=profile)
