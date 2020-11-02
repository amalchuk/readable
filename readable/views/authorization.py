from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.messages.api import success as add_success_message
from django.http.response import HttpResponse
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView

from readable.forms import AuthenticationForm
from readable.forms import UserCreationForm


class LoginView(BaseLoginView):
    form_class = AuthenticationForm
    http_method_names = ["get", "post"]
    redirect_authenticated_user = True
    template_name = "login.html"


class LogoutView(LoginRequiredMixin, BaseLogoutView):
    http_method_names = ["get"]

    def get_next_page(self) -> str:
        next_page = super(LogoutView, self).get_next_page()
        add_success_message(self.request, _("You have successfully logged out."))
        return next_page


class RegistrationView(CreateView):
    form_class = UserCreationForm
    http_method_names = ["get", "post"]
    success_url = reverse_lazy("index")
    template_name = "registration.html"

    def form_valid(self, form: UserCreationForm) -> HttpResponse:
        response = super(RegistrationView, self).form_valid(form)
        profile: User = getattr(self, "object")
        login(self.request, profile)
        return response


login_view = LoginView.as_view()
logout_view = LogoutView.as_view()
registration_view = RegistrationView.as_view()
