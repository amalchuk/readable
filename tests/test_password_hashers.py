from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import identify_hasher
from django.contrib.auth.hashers import is_password_usable
from django.contrib.auth.hashers import make_password
from django.test.testcases import SimpleTestCase as TestCase


class TestPasswordHashers(TestCase):
    def test_sha3_256(self) -> None:
        encoded = make_password("пронзительный", "seasalt", "sha3_256")
        self.assertEqual(encoded, "sha3_256$seasalt$44ae80375715b4b371d69f89944a1d68582a8756c7df3790de4dbb37a5230b6e")
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(check_password("пронзительный", encoded))
        self.assertFalse(check_password("пронизывающий", encoded))
        self.assertEqual(identify_hasher(encoded).algorithm, "sha3_256")
