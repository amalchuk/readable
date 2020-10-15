from typing import Any

from django.db.utils import DatabaseError
from django.utils.timezone import now

from readable.models import Documents, Staff
from readable.tasks import file_processing
from readable.utils.decorators import no_exception


@no_exception(AttributeError, DatabaseError)
def user_logged_in_out(*args: Any, **kwargs: Any) -> None:  # pragma: no cover
    """
    Sent when the ``login`` and ``logout`` methods is called.
    """
    Staff.objects.update_or_create(user=kwargs["user"], defaults={
        "user_agent": kwargs["request"].META.get("HTTP_USER_AGENT", None),
        "ip_address": kwargs["request"].META.get("REMOTE_ADDR", None)
    })


def documents_uploaded(*args: Any, **kwargs: Any) -> None:
    instance: Documents = kwargs.pop("instance")

    if instance.unavailable:
        status = Documents.Status.IN_PROGRESS
        Documents.objects.filter(id=instance.id).update(status=status, updated_at=now())
        file_processing.delay(instance.id)
