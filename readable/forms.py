from typing import Final
from unicodedata import normalize

from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.models import User
from django.db.models.base import Model as BaseModel
from django.forms.fields import CharField
from django.forms.fields import FileField
from django.forms.models import ModelForm as Form
from django.utils.translation import gettext_lazy as _

from readable.models import Documents
from readable.utils.collections import as_list
from readable.utils.validators import validate_ascii_username
from readable.utils.validators import validate_filename

__all__: Final[list[str]] = ["AuthenticationForm", "DocumentsForm", "UserCreationForm", "UserForm"]


class DocumentsForm(Form):
    filename = FileField(validators=as_list(validate_filename), error_messages={
        "required": _("No file was submitted.")
    })

    class Meta:
        model: type[BaseModel] = Documents
        fields: list[str] = as_list("filename")


class AuthenticationForm(BaseAuthenticationForm):
    def clean_username(self) -> str:
        """
        All case-based characters of the username field will be lowercased.
        """
        username: str = normalize("NFKC", self.cleaned_data["username"])
        return username.lower() if not username.islower() else username


class UserCreationForm(BaseUserCreationForm):
    username = CharField(label=_("Login"), min_length=6, max_length=50, validators=as_list(validate_ascii_username))

    class Meta:
        model: type[BaseModel] = User
        fields: list[str] = as_list("username")

    def clean_username(self) -> str:
        """
        All case-based characters of the username field will be lowercased.
        """
        username: str = self.cleaned_data["username"]
        return username.lower() if not username.islower() else username


class UserForm(Form):
    class Meta:
        model: type[BaseModel] = User
        fields: list[str] = ["first_name", "last_name", "email"]
