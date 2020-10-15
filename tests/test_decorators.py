from django.test.testcases import SimpleTestCase as TestCase

from readable.utils.decorators import no_exception


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
