from typing import Any

from django.db.utils import DatabaseError

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
    is_created: bool = kwargs.pop("created")
    instance: Documents = kwargs.pop("instance")

    if is_created and instance.unavailable:
        file_processing.delay(instance.id)
