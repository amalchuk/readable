from atexit import register
from pathlib import PurePath as _P
from shutil import rmtree as delete
from tempfile import mkdtemp as _temporary_directory


def temporary_directory() -> _P:
    """
    Create a unique temporary directory.
    """
    directory = _temporary_directory(prefix="readable")
    register(delete, directory, ignore_errors=True)
    return _P(directory)
