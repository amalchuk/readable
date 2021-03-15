from typing import Final, Iterator, List, Tuple, TypeVar

__all__: Final[List[str]] = ["as_iterable", "as_list", "as_tuple"]

T = TypeVar("T")


def as_iterable(obj: T, /, *args: T) -> Iterator[T]:
    """
    Return an ``iterable`` containing only the specified ``object``.
    """
    yield obj
    yield from args


def as_list(obj: T, /, *args: T) -> List[T]:
    """
    Return a ``list`` containing only the specified ``object``.
    """
    return list(as_iterable(obj, *args))


def as_tuple(obj: T, /, *args: T) -> Tuple[T, ...]:
    """
    Return a ``tuple`` containing only the specified ``object``.
    """
    return tuple(as_iterable(obj, *args))
