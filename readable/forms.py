from unicodedata import normalize

from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.models import User
from django.forms.fields import CharField
from django.forms.fields import FileField
from django.forms.models import ModelForm as Form
from django.utils.translation import gettext_lazy as _

from readable.models import Documents
from readable.utils.validators import validate_filename
from readable.utils.validators import validate_username


class DocumentsForm(Form):
    filename = FileField(validators=[validate_filename], error_messages={
        "required": _("No file was submitted.")
    })

    class Meta:
        model = Documents
        fields = ["filename"]


class AuthenticationForm(BaseAuthenticationForm):
    def clean_username(self) -> str:
        """
        All case-based characters of the username field will be lowercased.
        """
        return normalize("NFKC", self.cleaned_data["username"]).lower()


class UserCreationForm(BaseUserCreationForm):
    username = CharField(label=_("Login"), min_length=6, max_length=50, validators=[validate_username])

    class Meta:
        model = User
        fields = ["username"]

    def clean_username(self) -> str:
        """
        All case-based characters of the username field will be lowercased.
        """
        return self.cleaned_data["username"].lower()


class UserForm(Form):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
