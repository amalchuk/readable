from typing import TypeVar

T = TypeVar("T")


def clamp(value: T, min_value: T, max_value: T) -> T:
    """
    Limits a provided value between two specified bounds.
    """
    return max(min_value, min(value, max_value))
