import re
from itertools import chain, product
from typing import Iterator

from readable.utils.decorators import cacheable

russian_lowercase = "".join(map(chr, chain(range(1072, 1078), [1105], range(1078, 1104))))
russian_uppercase = "".join(map(chr, chain(range(1040, 1046), [1025], range(1046, 1072))))
russian_letters = russian_lowercase + russian_uppercase

sentences_pattern = re.compile("\x28\x5B\x2E\x3F\x21\u2026\x5D\x29\x5C\x73\x2B", re.UNICODE)
words_pattern = re.compile("\x28\x5B\x5E\x5C\x57\x5C\x64\x5D\x2B\x7C\x5C\x64\x2B\x7C\x5B\x5E\x5C\x77\x5C\x73\x5D\x29", re.UNICODE)


def sentences(text: str) -> Iterator[str]:
    """
    Tokenize a paragraph into sentences.
    """
    previous = 0

    for match in sentences_pattern.finditer(text):
        delimiter = match.group(1)
        start = match.start()

        yield text[previous:start] + delimiter
        previous = match.end()

    if previous < len(text):
        yield text[previous:]


def words(sentence: str) -> Iterator[str]:
    """
    Tokenize a sentence into words.
    """
    for match in words_pattern.finditer(sentence):
        if (word := match.group(1)).isalnum():
            yield word


@cacheable
def syllables(word: str) -> int:
    """
    Return the number of syllables in a word.
    """
    lower_word = word.lower()

    # Russian vowels:
    vowels = "\u0430\u0435\u0451\u0438\u043E\u0443\u044B\u044D\u044E\u044F"

    if any(vowel in lower_word for vowel in vowels):
        return sum(map(lower_word.count, vowels))

    # English vowels:
    vowels = "\x61\x65\x69\x6F\x75\x79"
    count = 0

    if any(vowel in lower_word for vowel in vowels):
        count += sum(map(lower_word.count, vowels))
        count -= lower_word.endswith("\x65")

        diphthongs: Iterator[str] = map("".join, product(vowels, repeat=2))
        count -= sum(map(lower_word.count, diphthongs))

        triphthongs: Iterator[str] = map("".join, product(vowels, repeat=3))
        count -= sum(map(lower_word.count, triphthongs))

        if lower_word.endswith("\x6C\x65") or lower_word.endswith("\x6C\x65\x73"):
            lower_word, _ = lower_word.split("\x6C\x65", 1)
            count += all(not lower_word.endswith(vowel) for vowel in vowels)

    return count or 1
