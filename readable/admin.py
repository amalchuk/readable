from typing import Any, Final, Optional

from django.contrib.admin.decorators import register
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.options import StackedInline
from django.contrib.admin.sites import site as default_site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models.base import Model as BaseModel
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from readable.models import Documents
from readable.models import Metrics
from readable.models import Staff
from readable.types import FieldSetsType
from readable.utils.collections import as_list

__all__: Final[list[str]] = ["DocumentsAdmin", "MetricsInline", "StaffInline", "UserAdmin"]

# Re-register UserAdmin:
default_site.unregister(User)


class StaffInline(StackedInline):
    can_delete: bool = False
    model: type[BaseModel] = Staff
    readonly_fields: list[str] = ["user_agent", "ip_address"]
    fieldsets: FieldSetsType = [
        (None, {
            "fields": ["user_agent", "ip_address"]
        })
    ]


@register(User)
class UserAdmin(BaseUserAdmin):
    def get_inlines(self, request: HttpRequest, obj: Optional[User], /) -> list[type[InlineModelAdmin]]:
        return super(UserAdmin, self).get_inlines(request, obj) if obj is None else as_list(StaffInline)


class MetricsInline(StackedInline):
    can_delete: bool = False
    model: type[BaseModel] = Metrics
    readonly_fields: list[str] = ["is_russian", "sentences", "words", "letters", "syllables"]
    fieldsets: FieldSetsType = [
        (None, {
            "fields": ["is_russian", "sentences", "words", "letters", "syllables"]
        })
    ]


@register(Documents)
class DocumentsAdmin(ModelAdmin):
    date_hierarchy: str = "created_at"
    list_display: list[str] = ["id", "realname", "status", "created_at", "updated_at"]
    list_filter: list[str] = ["status"]
    readonly_fields: list[str] = ["realname", "status", "uploaded_by", "created_at", "updated_at"]
    fieldsets: FieldSetsType = [
        (_("Primary fields"), {
            "fields": ["filename", "status", "uploaded_by"]
        })
    ]
    add_fieldsets: FieldSetsType = [
        (None, {
            "fields": ["filename"],
            "classes": ["wide"]
        })
    ]

    def has_change_permission(self, request: HttpRequest, obj: Optional[Documents] = None, /) -> bool:
        return request.user.is_superuser and obj is not None and obj.unavailable

    def has_delete_permission(self, request: HttpRequest, obj: Optional[Documents] = None, /) -> bool:
        return request.user.is_superuser and obj is not None and obj.unavailable

    def get_fieldsets(self, request: HttpRequest, obj: Optional[Documents] = None, /) -> FieldSetsType:
        return self.add_fieldsets if obj is None else super(DocumentsAdmin, self).get_fieldsets(request, obj)

    def get_inlines(self, request: HttpRequest, obj: Optional[Documents], /) -> list[type[InlineModelAdmin]]:
        return super(DocumentsAdmin, self).get_inlines(request, obj) if obj is None else as_list(MetricsInline)

    def get_queryset(self, request: HttpRequest, /) -> "QuerySet[Documents]":
        qs: "QuerySet[Documents]" = super(DocumentsAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(uploaded_by__user=request.user)

    def save_model(self, request: HttpRequest, obj: Documents, /, *args: Any, **kwargs: Any) -> None:
        obj.uploaded_by = request.user.staff
        obj.save()
