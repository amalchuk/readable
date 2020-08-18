from readable.utils.comparable import clamp
from readable.utils.decorators import no_exception


@no_exception(ZeroDivisionError, default=0.0)
def flesch_reading_ease_score(sentences: int, words: int, syllables: int) -> float:
    value = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    return clamp(value, 0.0, 100.0)


@no_exception(ZeroDivisionError, default=0.0)
def automated_readability_index(sentences: int, words: int, letters: int) -> float:
    value = 4.71 * (letters / words) + 0.5 * (words / sentences) - 21.43
    return max(0.0, value)


@no_exception(ZeroDivisionError, default=0.0)
def coleman_liau_index(sentences: int, words: int, letters: int) -> float:
    value = 0.0588 * (letters / words * 100.0) - 0.296 * (sentences / words * 100.0) - 15.8
    return max(0.0, value)


def overall_index(flesch_reading_ease_score: float, automated_readability_index: float, coleman_liau_index: float) -> float:
    flesch_reading_ease_score /= 100.0
    automated_readability_index = 1.0 - clamp(automated_readability_index, 5.0, 14.0) / 14.0
    coleman_liau_index = 1.0 - clamp(coleman_liau_index, 6.0, 16.0) / 16.0

    value = (flesch_reading_ease_score + automated_readability_index + coleman_liau_index) / 3.0 * 100.0
    return clamp(value, 0.0, 100.0)
