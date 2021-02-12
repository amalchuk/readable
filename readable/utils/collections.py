from typing import Final, Iterator, List, Tuple, TypeVar

__all__: Final[List[str]] = ["as_iterable", "as_list", "as_tuple"]

T = TypeVar("T")


def as_iterable(obj: T, /) -> Iterator[T]:
    """
    Return an ``iterable`` containing only the specified ``object``.
    """
    yield obj


def as_list(obj: T, /) -> List[T]:
    """
    Return a ``list`` containing only the specified ``object``.
    """
    return list(as_iterable(obj))


def as_tuple(obj: T, /) -> Tuple[T, ...]:
    """
    Return a ``tuple`` containing only the specified ``object``.
    """
    return tuple(as_iterable(obj))
