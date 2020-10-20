import re

from django.core.validators import FileExtensionValidator
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

validate_username = RegexValidator(
    regex=r"^[a-zA-Z0-9]+$",
    flags=re.ASCII,
    message=_("The username should contain only Latin letters and digits 0 to 9."))

validate_filename = FileExtensionValidator(
    allowed_extensions=["docx", "pdf", "txt"],
    message=_("Invalid file extension. Only \".docx\", \".pdf\" and \".txt\" are allowed."))
