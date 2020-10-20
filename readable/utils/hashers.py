from hashlib import new as hash_new
from secrets import compare_digest as constant_time_compare
from secrets import token_hex as get_random_string
from typing import Dict

from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.translation import gettext_noop as _


class SHA256PasswordHasher(BasePasswordHasher):
    algorithm = "sha3_256"
    encoding = "utf-8"

    def salt(self) -> str:  # pragma: no cover
        return get_random_string(0b110)

    def verify(self, password: str, encoded: str) -> bool:
        algorithm, salt, _ = encoded.split("\x24", 0b10)
        assert algorithm == self.algorithm
        to_verify = self.encode(password, salt).encode(self.encoding)
        return constant_time_compare(encoded.encode(self.encoding), to_verify)

    def encode(self, password: str, salt: str) -> str:
        assert password is not None
        assert salt and "\x24" not in salt
        hash_object = hash_new(self.algorithm)
        hash_object.update(f"{salt}{password}".encode(self.encoding))
        value = hash_object.hexdigest()
        return f"{self.algorithm}\x24{salt}\x24{value}"

    def safe_summary(self, encoded: str) -> Dict[str, str]:  # pragma: no cover
        algorithm, salt, value = encoded.split("\x24", 0b10)
        assert algorithm == self.algorithm
        return {
            _("algorithm"): algorithm,
            _("salt"): f"{salt[:0b10]}\u2026",
            _("hash"): f"{value[:0b110]}\u2026"
        }
