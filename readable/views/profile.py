from typing import Optional

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.api import success as add_success_message
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import UpdateView

from readable.forms import UserForm


@method_decorator(login_required, name="dispatch")
class ProfileView(UpdateView):
    form_class = UserForm
    success_url = reverse_lazy("profile")
    template_name = "profile.html"

    def form_valid(self, form: UserForm) -> HttpResponse:
        response = super(ProfileView, self).form_valid(form)
        add_success_message(self.request, _("Your account has been successfully updated."))
        return response

    def get_object(self, queryset: Optional[QuerySet] = None) -> User:
        return self.request.user


profile_view = ProfileView.as_view()
