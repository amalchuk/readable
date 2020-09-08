from concurrent.futures import Future
from functools import wraps
from typing import Any, Callable, Type, TypeVar, cast

from django.conf import settings
from django.http.response import HttpResponse

from readable.utils.executors import ThreadPoolExecutor

F = TypeVar("F", bound=Callable[..., Any])
R = TypeVar("R", bound=Callable[..., HttpResponse])
T = TypeVar("T")

sentinel = object()


def no_exception(*exceptions: Type[BaseException], default: Any = sentinel):
    def decorating_function(user_function: F) -> F:
        @wraps(user_function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return user_function(*args, **kwargs)

            except exceptions as exception:
                return exception if default is sentinel else default

        return cast(F, wrapper)
    return decorating_function


def run_in_executor(user_function: Callable[..., T]) -> "Callable[..., Future[T]]":
    executor: ThreadPoolExecutor[T] = settings.READABLE_POOL_EXECUTOR

    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> "Future[T]":
        return executor.submit(user_function, *args, **kwargs)

    return wrapper


def x_robots_tag(user_function: R) -> R:  # pragma: no cover
    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> HttpResponse:
        response = user_function(*args, **kwargs)
        response["X-Robots-Tag"] = ", ".join(("noindex", "noarchive"))
        return response

    return cast(R, wrapper)
