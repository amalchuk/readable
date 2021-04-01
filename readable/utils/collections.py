from typing import Final, Hashable, Iterator, TypeVar, Union

__all__: Final[list[str]] = ["as_frozenset", "as_iterable", "as_list", "as_set", "as_tuple"]

_T = TypeVar("_T")
_S = TypeVar("_S")
_HT = TypeVar("_HT", bound=Hashable)
_HS = TypeVar("_HS", bound=Hashable)


def as_iterable(item: _T, /, *items: _S) -> Iterator[Union[_T, _S]]:
    yield item
    yield from items


def as_tuple(item: _T, /, *items: _S) -> tuple[Union[_T, _S], ...]:
    return tuple(as_iterable(item, *items))


def as_list(item: _T, /, *items: _S) -> list[Union[_T, _S]]:
    return list(as_iterable(item, *items))


def as_set(item: _HT, /, *items: _HS) -> set[Union[_HT, _HS]]:
    return set(as_iterable(item, *items))


def as_frozenset(item: _HT, /, *items: _HS) -> frozenset[Union[_HT, _HS]]:
    return frozenset(as_iterable(item, *items))
