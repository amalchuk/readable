from typing import Iterable

from django.test.testcases import SimpleTestCase as TestCase

from readable.utils.collections import as_iterable
from readable.utils.collections import as_list
from readable.utils.collections import as_tuple


class TestCollections(TestCase):
    def test_as_iterable(self) -> None:
        sentinel = object()
        self.assertIsInstance(as_iterable(sentinel), Iterable)
        self.assertIn(sentinel, as_iterable(sentinel))

    def test_as_list(self) -> None:
        sentinel = object()
        self.assertListEqual([sentinel], as_list(sentinel))

    def test_as_tuple(self) -> None:
        sentinel = object()
        self.assertTupleEqual((sentinel,), as_tuple(sentinel))
