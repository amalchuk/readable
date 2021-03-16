from typing import Iterable

from django.test.testcases import SimpleTestCase as TestCase

from readable.utils.collections import as_frozenset
from readable.utils.collections import as_iterable
from readable.utils.collections import as_list
from readable.utils.collections import as_set
from readable.utils.collections import as_tuple


class TestCollections(TestCase):
    def test_as_iterable(self) -> None:
        sentinel = object()
        self.assertIsInstance(as_iterable(sentinel), Iterable)
        self.assertIn(sentinel, as_iterable(sentinel))
        self.assertIn(1, as_iterable(1, 2, 3))

    def test_as_tuple(self) -> None:
        sentinel = object()
        self.assertIsInstance(as_tuple(sentinel), tuple)
        self.assertIn(sentinel, as_tuple(sentinel))
        self.assertIn(1, as_tuple(1, 2, 3))
        self.assertTupleEqual((1, 2, 3), as_tuple(1, 2, 3))

    def test_as_list(self) -> None:
        sentinel = object()
        self.assertIsInstance(as_list(sentinel), list)
        self.assertIn(sentinel, as_list(sentinel))
        self.assertIn(1, as_list(1, 2, 3))
        self.assertListEqual([1, 2, 3], as_list(1, 2, 3))

    def test_as_set(self) -> None:
        sentinel = object()
        self.assertIsInstance(as_set(sentinel), set)
        self.assertIn(sentinel, as_set(sentinel))
        self.assertIn(1, as_set(1, 2, 3))
        self.assertSetEqual({1, 2, 3}, as_set(1, 2, 3))

    def test_as_frozenset(self) -> None:
        sentinel = object()
        self.assertIsInstance(as_frozenset(sentinel), frozenset)
        self.assertIn(sentinel, as_frozenset(sentinel))
        self.assertIn(1, as_frozenset(1, 2, 3))
        self.assertSetEqual(frozenset({1, 2, 3}), as_frozenset(1, 2, 3))
