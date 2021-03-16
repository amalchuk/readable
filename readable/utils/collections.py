from typing import Final, FrozenSet, Iterator, List, Set, Tuple, TypeVar, Union

__all__: Final[List[str]] = ["as_frozenset", "as_iterable", "as_list", "as_set", "as_tuple"]

_T = TypeVar("_T")
_S = TypeVar("_S")


def as_iterable(item: _T, /, *items: _S) -> Iterator[Union[_T, _S]]:
    yield item
    yield from items


def as_tuple(item: _T, /, *items: _S) -> Tuple[Union[_T, _S], ...]:
    return tuple(as_iterable(item, *items))


def as_list(item: _T, /, *items: _S) -> List[Union[_T, _S]]:
    return list(as_iterable(item, *items))


def as_set(item: _T, /, *items: _S) -> Set[Union[_T, _S]]:
    return set(as_iterable(item, *items))


def as_frozenset(item: _T, /, *items: _S) -> FrozenSet[Union[_T, _S]]:
    return frozenset(as_iterable(item, *items))
