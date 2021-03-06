from hashlib import sha3_256
from secrets import compare_digest as constant_time_compare
from secrets import token_hex as get_random_string
from typing import Final

from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.translation import gettext_noop as _

__all__: Final[list[str]] = ["SHA256PasswordHasher"]


class SHA256PasswordHasher(BasePasswordHasher):
    algorithm: Final[str] = "sha3_256"
    encoding: Final[str] = "utf-8"

    def salt(self) -> str:
        return get_random_string(0b110)

    def verify(self, password: str, encoded: str, /) -> bool:
        algorithm, salt, _ = encoded.split("\x24", 0b10)
        assert algorithm == self.algorithm
        to_verify: bytes = self.encode(password, salt).encode(self.encoding)
        return constant_time_compare(encoded.encode(self.encoding), to_verify)

    def encode(self, password: str, salt: str, /) -> str:
        assert password is not None
        assert salt and "\x24" not in salt
        value: str = sha3_256(f"{salt}{password}".encode(self.encoding)).hexdigest()
        return f"{self.algorithm}\x24{salt}\x24{value}"

    def safe_summary(self, encoded: str, /) -> dict[str, str]:
        algorithm, salt, value = encoded.split("\x24", 0b10)
        assert algorithm == self.algorithm
        return {
            _("algorithm"): algorithm,
            _("salt"): f"{salt[:0b10]}\u2026",
            _("hash"): f"{value[:0b110]}\u2026"
        }
