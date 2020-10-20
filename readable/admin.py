from typing import Any, Dict, List, Optional, Tuple

from django.contrib.admin.decorators import register
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.options import StackedInline
from django.contrib.admin.sites import site as default_site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from readable.models import Documents
from readable.models import Metrics
from readable.models import Staff

# Re-register UserAdmin:
default_site.unregister(User)


class StaffInline(StackedInline):
    can_delete = False
    model = Staff
    readonly_fields = ["user_agent", "ip_address"]
    fieldsets = [
        (None, {
            "fields": ["user_agent", "ip_address"]
        })
    ]


@register(User)
class UserAdmin(BaseUserAdmin):
    def get_inlines(self, request: HttpRequest, obj: Optional[User]) -> List[InlineModelAdmin]:
        inlines: List[InlineModelAdmin] = super(UserAdmin, self).get_inlines(request, obj).copy()
        if obj:
            inlines.append(StaffInline)
        return inlines


class MetricsInline(StackedInline):
    can_delete = False
    model = Metrics
    readonly_fields = ["is_russian", "sentences", "words", "letters", "syllables"]
    fieldsets = [
        (None, {
            "fields": ["is_russian", "sentences", "words", "letters", "syllables"]
        })
    ]


@register(Documents)
class DocumentsAdmin(ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ["id", "realname", "status", "created_at", "updated_at"]
    list_filter = ["status"]
    readonly_fields = ["realname", "status", "uploaded_by", "created_at", "updated_at"]
    fieldsets = [
        (_("Primary fields"), {
            "fields": ["filename", "status", "uploaded_by"]
        })
    ]
    add_fieldsets = [
        (None, {
            "fields": ["filename"],
            "classes": ["wide"]
        })
    ]

    def has_change_permission(self, request: HttpRequest, obj: Optional[Documents] = None) -> bool:
        return request.user.is_superuser and obj is not None and obj.unavailable

    def has_delete_permission(self, request: HttpRequest, obj: Optional[Documents] = None) -> bool:
        return request.user.is_superuser and obj is not None and obj.unavailable

    def get_fieldsets(self, request: HttpRequest, obj: Optional[Documents] = None) -> List[Tuple[Optional[str], Dict[str, List[str]]]]:
        return self.add_fieldsets if not obj else super(DocumentsAdmin, self).get_fieldsets(request, obj)

    def get_inlines(self, request: HttpRequest, obj: Optional[Documents]) -> List[InlineModelAdmin]:
        inlines: List[InlineModelAdmin] = super(DocumentsAdmin, self).get_inlines(request, obj).copy()
        if obj:
            inlines.append(MetricsInline)
        return inlines

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs: QuerySet = super(DocumentsAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(uploaded_by__user=request.user)

    def save_model(self, request: HttpRequest, obj: Documents, *args: Any, **kwargs: Any) -> None:
        if obj.status == Documents.Status.FINISHED:
            obj.status = Documents.Status.IN_PROGRESS

        obj.uploaded_by = request.user.staff
        obj.save()
