from concurrent.futures import Future
from operator import lshift, truediv
from typing import Any, Iterator

from django.test.testcases import SimpleTestCase as TestCase

from readable.utils.executors import ThreadPoolExecutor


class TestThreadPoolExecutor(TestCase):
    def setUp(self) -> None:
        self.executor: ThreadPoolExecutor[Any] = ThreadPoolExecutor()

    def test_submit(self) -> None:
        lshift_future: "Future[int]" = self.executor.submit(lshift, 1, 10)
        self.assertEqual(lshift_future.result(), 1 << 10)

        zero_division_future: "Future[float]" = self.executor.submit(truediv, 3.0, 0.0)
        self.assertIsInstance(zero_division_future.exception(), ZeroDivisionError)

    def test_apply(self) -> None:
        self.assertEqual(
            list(self.executor.apply(pow, range(10), range(10))),
            list(map(pow, range(10), range(10))))

        iterator: Iterator[float] = self.executor.apply(truediv, [1.0, 2.0, 3.0], [2.0, 5.0, 0.0])
        self.assertEqual(next(iterator), 0.5)
        self.assertEqual(next(iterator), 0.4)
        with self.assertRaises(ZeroDivisionError):
            next(iterator)
