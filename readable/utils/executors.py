from collections import deque
from concurrent.futures import Future, ThreadPoolExecutor as Executor
from multiprocessing import cpu_count
from threading import BoundedSemaphore as Semaphore
from typing import Any, Callable, Deque, Generic, Iterable, Iterator, Optional, TypeVar

R = TypeVar("R")


class ThreadPoolExecutor(Generic[R]):
    __slots__ = ("_max_queue_size", "_executor", "_semaphore")

    def __init__(self, *, max_queue_size: Optional[int] = None) -> None:
        self._max_queue_size = int(max_queue_size or cpu_count() * 2 + 1)
        self._executor = Executor(self._max_queue_size)
        self._semaphore = Semaphore(self._max_queue_size)

    def _acquire(self) -> None:
        """
        Acquire the semaphore.
        """
        self._semaphore.acquire()

    def _release(self, *args: Any, **kwargs: Any) -> None:
        """
        Release the semaphore.
        """
        self._semaphore.release()

    def submit(self, user_function: Callable[..., R], /, *args: Any, **kwargs: Any) -> "Future[R]":
        """
        Submit a ``user_function`` to be executed with the given arguments.
        """
        self._acquire()
        try:
            future = self._executor.submit(user_function, *args, **kwargs)

        except:
            self._release()
            raise

        else:
            future.add_done_callback(self._release)
            return future

    def apply(self, user_function: Callable[..., R], /, *iterables: Iterable[Any]) -> Iterator[R]:
        """
        Return an iterator equivalent to ``map(user_function, iterable)``.
        """
        queue: "Deque[Future[R]]" = deque()

        for args in zip(*iterables):
            future = self.submit(user_function, *args)
            queue.append(future)

        try:
            while queue:
                future = queue.popleft()
                yield future.result()

        finally:
            for future in queue:
                future.cancel()
