from concurrent.futures import Future
from operator import lshift
from typing import Any

from django.test.testcases import SimpleTestCase as TestCase

from readable.utils.executors import ThreadPoolExecutor


class TestThreadPoolExecutor(TestCase):
    def setUp(self) -> None:
        self.executor: ThreadPoolExecutor[Any] = ThreadPoolExecutor()

    def test_submit(self) -> None:
        future: "Future[int]" = self.executor.submit(lshift, 1, 10)
        self.assertEqual(future.result(), 1 << 10)

    def test_apply(self) -> None:
        self.assertEqual(
            list(self.executor.apply(pow, range(10), range(10))),
            list(map(pow, range(10), range(10))))
