from concurrent.futures import Future
from typing import Callable, TypeVar

from django.test.testcases import SimpleTestCase as TestCase

from readable.utils.decorators import no_exception, run_in_executor

R = TypeVar("R")


class TestDecorators(TestCase):
    def test_no_exception(self) -> None:
        @no_exception(ZeroDivisionError, default=None)
        def decorated(a: float, b: float) -> float:
            return a / b

        self.assertIs(decorated(10.0, 0.0), None)
        self.assertEqual(decorated(10.0, 2.0), 5.0)

        from importlib import import_module
        decorated = no_exception(ModuleNotFoundError)(import_module)
        self.assertNotIsInstance(decorated("sys"), ModuleNotFoundError)
        self.assertIsInstance(decorated("unknown_library"), ModuleNotFoundError)

    def test_run_in_executor(self) -> None:
        @run_in_executor
        def decorated(a: float, b: float) -> float:
            return a / b

        self.assertIsInstance(decorated(10.0, 2.0), Future)
        self.assertIsInstance(decorated(10.0, 0.0).exception(timeout=10.0), ZeroDivisionError)
