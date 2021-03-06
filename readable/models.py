from pathlib import Path as _P
from typing import Final
from uuid import uuid4 as uuid

from django.contrib.auth.models import User
from django.db.models.base import Model as BaseModel
from django.db.models.deletion import CASCADE
from django.db.models.enums import IntegerChoices
from django.db.models.fields import BooleanField
from django.db.models.fields import CharField
from django.db.models.fields import DateTimeField
from django.db.models.fields import GenericIPAddressField
from django.db.models.fields import IntegerField
from django.db.models.fields import UUIDField
from django.db.models.fields.files import FileField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.related import OneToOneField
from django.utils.text import get_valid_filename
from django.utils.translation import gettext_lazy as _
from scienco import Indexes
from scienco import compute_indexes

__all__: Final[list[str]] = ["Documents", "documents_upload_directory", "Metrics", "Staff"]


def documents_upload_directory(instance: "Documents", filename: str, /) -> str:
    instance.realname = get_valid_filename(filename)
    return f"{instance.id!s}{instance.path.suffix}"


class Model(BaseModel):
    id = UUIDField(verbose_name=_("UUID"), primary_key=True, default=uuid, editable=False)
    created_at = DateTimeField(verbose_name=_("Created at"), db_index=True, auto_now_add=True)
    updated_at = DateTimeField(verbose_name=_("Updated at"), db_index=True, auto_now=True)

    class Meta:
        abstract: bool = True


class Staff(Model):
    user = OneToOneField(verbose_name=_("User"), to=User, on_delete=CASCADE, related_name="staff")
    user_agent = CharField(verbose_name=_("User agent"), max_length=255, blank=True, null=True)
    ip_address = GenericIPAddressField(verbose_name=_("IP address"), unpack_ipv4=True, blank=True, null=True)

    class Meta:
        verbose_name: str = _("User's additional information")
        verbose_name_plural: str = _("Users' additional information")
        ordering: list[str] = ["-created_at", "-updated_at"]

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
        verbose_name: str = _("Document")
        verbose_name_plural: str = _("Documents")
        ordering: list[str] = ["-created_at", "-updated_at"]

    def __str__(self) -> str:
        return f"{self.realname}"

    @property
    def unavailable(self) -> bool:
        return self.status != self.Status.FINISHED

    @property
    def path(self) -> _P:
        return _P(self.filename.path)


class Metrics(Model):
    document = OneToOneField(verbose_name=_("Document"), to=Documents, on_delete=CASCADE, related_name="metrics")
    is_russian = BooleanField(verbose_name=_("Is Russian"), default=False)
    sentences = IntegerField(verbose_name=_("Sentences"), default=0)
    words = IntegerField(verbose_name=_("Words"), default=0)
    letters = IntegerField(verbose_name=_("Letters"), default=0)
    syllables = IntegerField(verbose_name=_("Syllables"), default=0)

    class Meta:
        verbose_name: str = _("Metric")
        verbose_name_plural: str = _("Metrics")
        ordering: list[str] = ["-created_at", "-updated_at"]

    def __str__(self) -> str:
        return f"{self.document}"

    @property
    def indexes(self) -> Indexes:  # pragma: no cover
        """
        Calculate the readability indexes.
        """
        return compute_indexes(self.sentences, self.words, self.letters, self.syllables, is_russian=self.is_russian)
