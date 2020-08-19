from typing import Any, Protocol, TypeVar, runtime_checkable

T = TypeVar("T", bound="Comparable")


@runtime_checkable
class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...


def clamp(value: T, min_value: T, max_value: T) -> T:
    """
    Limits a provided value between two specified bounds.
    """
    return max(min_value, min(value, max_value))
