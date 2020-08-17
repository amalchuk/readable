from functools import cached_property
from pathlib import Path
from uuid import uuid4 as uuid

from django.contrib.auth.models import User
from django.db.models.base import Model as BaseModel
from django.db.models.deletion import CASCADE
from django.db.models.enums import IntegerChoices
from django.db.models.fields import BooleanField, CharField, DateTimeField, GenericIPAddressField, IntegerField, UUIDField
from django.db.models.fields.files import FileField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.utils.text import get_valid_filename
from django.utils.translation import gettext_lazy as _


def documents_upload_directory(instance: "Documents", filename: str) -> str:
    instance.realname = get_valid_filename(filename)
    return f"{instance.id!s}{instance.path.suffix}"


class Model(BaseModel):
    id = UUIDField(verbose_name=_("UUID"), primary_key=True, default=uuid, editable=False)
    created_at = DateTimeField(verbose_name=_("Created at"), db_index=True, auto_now_add=True)
    updated_at = DateTimeField(verbose_name=_("Updated at"), db_index=True, auto_now=True)

    class Meta:
        abstract = True


class Staff(Model):
    user = OneToOneField(verbose_name=_("User"), to=User, on_delete=CASCADE, related_name="staff")
    user_agent = CharField(verbose_name=_("User agent"), max_length=255, blank=True, null=True)
    ip_address = GenericIPAddressField(verbose_name=_("IP address"), unpack_ipv4=True, blank=True, null=True)

    class Meta:
        verbose_name = _("User's additional information")
        verbose_name_plural = _("Users' additional information")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self) -> str:
        return f"{self.user}"


class Documents(Model):
    class Status(IntegerChoices):
        FAILED = (0, _("Failed"))
        CREATED = (1, _("Created"))
        IN_PROGRESS = (2, _("In progress"))
        FINISHED = (3, _("Finished"))

    filename = FileField(verbose_name=_("Document"), upload_to=documents_upload_directory)
    realname = CharField(verbose_name=_("Real name"), max_length=255, blank=True, null=True)
    status = IntegerField(verbose_name=_("Status"), default=Status.CREATED, choices=Status.choices)
    uploaded_by = ForeignKey(verbose_name=_("Uploaded by"), to=Staff, on_delete=CASCADE, related_name="documents")

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self) -> str:
        return f"{self.realname}"

    @property
    def unavailable(self) -> bool:
        return self.status != self.Status.FINISHED

    @property
    def path(self) -> Path:
        return Path(self.filename.path)  # pylint: disable=no-member


class Metrics(Model):
    document = OneToOneField(verbose_name=_("Document"), to=Documents, on_delete=CASCADE, related_name="metrics")
    is_russian = BooleanField(verbose_name=_("Is Russian"), default=False)
    sentences = IntegerField(verbose_name=_("Sentences"), default=0)
    words = IntegerField(verbose_name=_("Words"), default=0)
    letters = IntegerField(verbose_name=_("Letters"), default=0)
    syllables = IntegerField(verbose_name=_("Syllables"), default=0)

    class Meta:
        verbose_name = _("Metric")
        verbose_name_plural = _("Metrics")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self) -> str:
        return f"{self.document}"

    @cached_property
    def flesch_reading_ease_score(self) -> float:
        from readable.utils.plain_language.indexes import flesch_reading_ease_score as _
        return _(self.sentences, self.words, self.syllables, is_russian=self.is_russian)

    @cached_property
    def automated_readability_index(self) -> float:
        from readable.utils.plain_language.indexes import automated_readability_index as _
        return _(self.sentences, self.words, self.letters, is_russian=self.is_russian)

    @cached_property
    def coleman_liau_index(self) -> float:
        from readable.utils.plain_language.indexes import coleman_liau_index as _
        return _(self.sentences, self.words, self.letters, is_russian=self.is_russian)

    @cached_property
    def overall_index(self) -> float:
        from readable.utils.plain_language.indexes import overall_index as _
        return _(
            flesch_reading_ease_score=self.flesch_reading_ease_score,
            automated_readability_index=self.automated_readability_index,
            coleman_liau_index=self.coleman_liau_index,
            is_russian=self.is_russian)
