from atexit import register
from pathlib import PurePath as _P
from shutil import rmtree as delete
from tempfile import mkdtemp as _temporary_directory
from typing import Final, Optional

__all__: Final[list[str]] = ["temporary_directory"]


def temporary_directory(*, prefix: Optional[str] = None, ignore_errors: bool = True) -> _P:
    """
    Create a unique temporary directory.
    """
    directory: str = _temporary_directory(prefix=prefix)
    register(delete, directory, ignore_errors=ignore_errors)
    return _P(directory)
