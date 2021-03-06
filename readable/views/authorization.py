from typing import Final

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.messages.api import success as add_success_message
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView

from readable.forms import AuthenticationForm
from readable.forms import UserCreationForm
from readable.types import ViewType

__all__: Final[list[str]] = ["login_view", "logout_view", "registration_view"]


class LoginView(BaseLoginView):
    form_class: type[BaseForm] = AuthenticationForm
    http_method_names: list[str] = ["get", "post"]
    redirect_authenticated_user: bool = True
    template_name: str = "login.html"


class LogoutView(LoginRequiredMixin, BaseLogoutView):
    http_method_names: list[str] = ["get"]

    def get_next_page(self) -> str:
        next_page: str = super(LogoutView, self).get_next_page()
        add_success_message(self.request, _("You have successfully logged out."))
        return next_page


class RegistrationView(CreateView):
    form_class: type[BaseForm] = UserCreationForm
    http_method_names: list[str] = ["get", "post"]
    success_url: str = reverse_lazy("index")
    template_name: str = "registration.html"

    def form_valid(self, form: UserCreationForm) -> HttpResponse:
        response: HttpResponse = super(RegistrationView, self).form_valid(form)
        profile: User = getattr(self, "object")
        login(self.request, profile)
        return response


login_view: Final[ViewType] = LoginView.as_view()
logout_view: Final[ViewType] = LogoutView.as_view()
registration_view: Final[ViewType] = RegistrationView.as_view()
