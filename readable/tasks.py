from uuid import UUID

from django.utils.timezone import now
from scienco import compute_metrics

from readable import celery
from readable.models import Documents, Metrics
from readable.utils.read_documents import read_document


@celery.task
def file_processing(uuid: UUID) -> None:
    status = Documents.Status.IN_PROGRESS
    updated_at = now()
    Documents.objects.filter(id=uuid).update(status=status, updated_at=updated_at)

    document = Documents.objects.get(id=uuid)
    text = read_document(document.path)
    is_finished = False

    if text:
        metrics = compute_metrics(text)
        Metrics.objects.update_or_create(document=document, defaults={
            "sentences": metrics.sentences,
            "words": metrics.words,
            "letters": metrics.letters,
            "syllables": metrics.syllables,
            "is_russian": metrics.is_russian
        })
        is_finished = True

    status = Documents.Status.FINISHED if is_finished else Documents.Status.FAILED
    updated_at = now()
    Documents.objects.filter(id=uuid).update(status=status, updated_at=updated_at)
