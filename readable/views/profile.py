from typing import Callable, Final, List, Optional, Type

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.api import success as add_success_message
from django.db.models.query import QuerySet
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import UpdateView

from readable.forms import UserForm

__all__: Final[List[str]] = ["profile_view"]


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class: Type[BaseForm] = UserForm
    http_method_names: List[str] = ["get", "post"]
    success_url: str = reverse_lazy("profile")
    template_name: str = "profile.html"

    def form_valid(self, form: UserForm) -> HttpResponse:
        response: HttpResponse = super(ProfileView, self).form_valid(form)
        add_success_message(self.request, _("Your account has been successfully updated."))
        return response

    def get_object(self, queryset: Optional["QuerySet[User]"] = None) -> User:
        return self.request.user


profile_view: Callable[..., HttpResponse] = ProfileView.as_view()
