from atexit import register
from pathlib import PurePath as _P
from shutil import rmtree as delete
from tempfile import mkdtemp as _temporary_directory
from typing import Final, List, Optional

__all__: Final[List[str]] = ["temporary_directory"]


def temporary_directory(*, prefix: Optional[str] = None) -> _P:
    """
    Create a unique temporary directory.
    """
    directory = _temporary_directory(prefix=prefix)
    register(delete, directory, ignore_errors=True)
    return _P(directory)
