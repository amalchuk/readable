from uuid import UUID

from django.utils.timezone import now
from scienco import compute_metrics

from readable import celery
from readable.models import Documents, Metrics
from readable.utils.read_documents import read_document


@celery.task
def file_processing(instance_id: UUID) -> None:
    instance = Documents.objects.get(id=instance_id)
    text = read_document(instance.path)
    is_finished = False

    if text:
        metrics = compute_metrics(text)
        Metrics.objects.update_or_create(document=instance, defaults={
            "sentences": metrics.sentences,
            "words": metrics.words,
            "letters": metrics.letters,
            "syllables": metrics.syllables,
            "is_russian": metrics.is_russian
        })
        is_finished = True

    status = Documents.Status.FINISHED if is_finished else Documents.Status.FAILED
    Documents.objects.filter(id=instance_id).update(status=status, updated_at=now())
