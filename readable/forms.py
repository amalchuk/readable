from unicodedata import normalize

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.fields import CharField, FileField
from django.forms.models import ModelForm as Form
from django.utils.translation import gettext_lazy as _

from readable.models import Documents
from readable.utils.validators import validate_filename, validate_username


class DocumentsForm(Form):
    filename = FileField(validators=[validate_filename], error_messages={
        "required": _("No file was submitted.")
    })

    class Meta:
        model = Documents
        fields = ["filename"]


class AuthorizationForm(AuthenticationForm):
    def clean_username(self) -> str:
        """
        All case-based characters of the username field will be lowercased.
        """
        return normalize("NFKC", self.cleaned_data["username"]).lower()


class RegistrationForm(UserCreationForm):
    username = CharField(label=_("Login"), min_length=6, max_length=50, validators=[validate_username])

    class Meta:
        model = User
        fields = ["username"]

    def clean_username(self) -> str:
        """
        All case-based characters of the username field will be lowercased.
        """
        return normalize("NFKC", self.cleaned_data["username"]).lower()


class UserForm(Form):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_first_name(self) -> str:
        """
        The first character of the first_name field will be capitalized.
        """
        return normalize("NFKC", self.cleaned_data["first_name"]).title()

    def clean_last_name(self) -> str:
        """
        The first character of the last_name field will be capitalized.
        """
        return normalize("NFKC", self.cleaned_data["last_name"]).title()

    def clean_email(self) -> str:
        """
        All case-based characters will be lowercased.
        """
        return normalize("NFKC", self.cleaned_data["email"]).lower()
