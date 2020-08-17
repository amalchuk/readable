from itertools import chain
from string import ascii_letters
from typing import Any, TypedDict

from django.conf import settings

from readable.utils.executors import ThreadPoolExecutor
from readable.utils.plain_language import processing


class Metrics(TypedDict):
    is_russian: bool
    sentences: int
    words: int
    letters: int
    syllables: int


def compute(text: str) -> Metrics:
    executor: ThreadPoolExecutor[Any] = settings.READABLE_POOL_EXECUTOR

    russian_letters = sum(executor.apply(text.count, processing.russian_letters))
    english_letters = sum(executor.apply(text.count, ascii_letters))
    sentences = tuple(processing.sentences(text))
    words = tuple(chain.from_iterable(executor.apply(processing.words, sentences)))

    return {
        "is_russian": russian_letters > english_letters,
        "sentences": len(sentences),
        "words": len(words),
        "letters": sum(executor.apply(len, words)),
        "syllables": sum(executor.apply(processing.syllables, words))
    }
