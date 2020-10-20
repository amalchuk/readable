from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.messages.api import success as add_success_message
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView

from readable.forms import AuthorizationForm
from readable.forms import RegistrationForm


class LoginView(BaseLoginView):
    form_class = AuthorizationForm
    template_name = "login.html"


@method_decorator(login_required, name="dispatch")
class LogoutView(BaseLogoutView):
    def get_next_page(self) -> str:
        next_page = super(LogoutView, self).get_next_page()
        add_success_message(self.request, _("You have successfully logged out."))
        return next_page


class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy("login")
    template_name = "registration.html"


login_view = LoginView.as_view()
logout_view = LogoutView.as_view()
registration_view = RegistrationView.as_view()
