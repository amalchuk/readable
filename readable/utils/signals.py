from concurrent.futures import Future
from typing import Any, Optional, Tuple, Union

from django.db.utils import DatabaseError
from django.utils.timezone import now as utcnow
from scienco import compute_metrics

from readable.models import Documents, Metrics, Staff
from readable.utils.decorators import no_exception, run_in_executor
from readable.utils.read_documents import read_document

ProcessingReturn = Tuple[Documents, Union[Metrics, Exception, None]]


@no_exception(AttributeError, DatabaseError)
def user_logged_in_out(*args: Any, **kwargs: Any) -> None:  # pragma: no cover
    """
    Sent when the ``login`` and ``logout`` methods is called.
    """
    Staff.objects.update_or_create(user=kwargs["user"], defaults={
        "user_agent": kwargs["request"].META.get("HTTP_USER_AGENT", None),
        "ip_address": kwargs["request"].META.get("REMOTE_ADDR", None)
    })


@run_in_executor
def file_processing(instance: Documents) -> ProcessingReturn:
    def update_or_create() -> Optional[Metrics]:
        if (text := read_document(instance.path)):
            metrics = compute_metrics(text)
            obj, _ = Metrics.objects.update_or_create(document=instance, defaults={
                "sentences": metrics.sentences,
                "words": metrics.words,
                "letters": metrics.letters,
                "syllables": metrics.syllables,
                "is_russian": metrics.is_russian
            })
            return obj

        return None
    return instance, update_or_create()


def file_processing_finished(future: "Future[ProcessingReturn]") -> None:
    instance, metrics = future.result()
    update_fields = {
        "status": Documents.Status.FINISHED if isinstance(metrics, Metrics) else Documents.Status.FAILED,
        "updated_at": utcnow()
    }
    Documents.objects.filter(id=instance.id).update(**update_fields)


def documents_uploaded(*args: Any, **kwargs: Any) -> None:
    instance: Documents = kwargs.pop("instance")

    if instance.unavailable:
        update_fields = {
            "status": Documents.Status.IN_PROGRESS,
            "updated_at": utcnow()
        }
        Documents.objects.filter(id=instance.id).update(**update_fields)
        future = file_processing(instance)
        future.add_done_callback(file_processing_finished)  # pylint: disable=no-member
