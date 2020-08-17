from concurrent.futures import Future
from functools import wraps
from hashlib import sha256
from typing import Any, Callable, Type, TypeVar, cast

from django.conf import settings
from django.core.cache import caches
from django.core.serializers.json import DjangoJSONEncoder as JSONEncoder

from readable.utils.executors import ThreadPoolExecutor

F = TypeVar("F", bound=Callable[..., Any])
R = TypeVar("R")

sentinel = object()


def cacheable(user_function: F) -> F:
    def generate_serialized_key(function_name: str, *args: Any, **kwargs: Any) -> str:
        encoder = JSONEncoder(ensure_ascii=False, sort_keys=True, separators=("\x00", "\x00"))
        hash_object = sha256(encoder.encode(args).encode("utf-8"))
        hash_object.update(encoder.encode(kwargs).encode("utf-8"))
        value = hash_object.hexdigest()
        return f"{function_name}\x24{value}"

    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        internal_cache = caches[settings.READABLE_INTERNAL_CACHE_ALIAS]
        function_name = getattr(user_function, "__name__")
        serialized_key = generate_serialized_key(function_name, *args, **kwargs)

        if not internal_cache.has_key(serialized_key):
            value = user_function(*args, **kwargs)
            internal_cache.set(serialized_key, value)
            return value

        return internal_cache.get(serialized_key)
    return cast(F, wrapper)


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


def run_in_executor(user_function: Callable[..., R]) -> "Callable[..., Future[R]]":
    executor: ThreadPoolExecutor[R] = settings.READABLE_POOL_EXECUTOR

    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> "Future[R]":
        return executor.submit(user_function, *args, **kwargs)

    return wrapper
