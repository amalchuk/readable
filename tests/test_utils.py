from django.test.testcases import SimpleTestCase as TestCase

from readable.utils import clamp


class TestUtils(TestCase):
    def test_clamp(self) -> None:
        self.assertEqual(clamp(0.0, 1.0, 2.0), 1.0)
        self.assertEqual(clamp(1.0, 1.0, 2.0), 1.0)
        self.assertEqual(clamp(2.0, 1.0, 2.0), 2.0)
        self.assertEqual(clamp(3.0, 1.0, 2.0), 2.0)

        self.assertEqual(clamp("a", "b", "c"), "b")
        self.assertEqual(clamp("b", "b", "c"), "b")
        self.assertEqual(clamp("c", "b", "c"), "c")
        self.assertEqual(clamp("d", "b", "c"), "c")
