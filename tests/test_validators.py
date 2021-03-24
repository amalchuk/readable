from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError

from readable.public_api.utils.validators import validate_unique_username

from .utils import TestCase


class TestValidators(TestCase):
    def test_validate_unique_username(self) -> None:
        user: User = self.create_user("staff", self.get_random_string())

        with self.assertRaises(ValidationError):
            validate_unique_username(user.username)

        try:
            validate_unique_username(None)  # type: ignore
        except ValidationError as exception:
            self.fail(exception)
