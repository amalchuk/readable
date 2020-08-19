from readable.utils.plain_language.indexes import english, russian


def flesch_reading_ease_score(
    sentences: int,
    words: int,
    syllables: int,
    *,
    is_russian: bool = False
) -> float:
    """
    Calculate the Flesch-Kincaid score.
    """
    _ = russian.flesch_reading_ease_score if is_russian else english.flesch_reading_ease_score
    return _(sentences, words, syllables)


def automated_readability_index(
    sentences: int,
    words: int,
    letters: int,
    *,
    is_russian: bool = False
) -> float:
    """
    Calculate the Automated readability index.
    """
    _ = russian.automated_readability_index if is_russian else english.automated_readability_index
    return _(sentences, words, letters)


def coleman_liau_index(
    sentences: int,
    words: int,
    letters: int,
    *,
    is_russian: bool = False
) -> float:
    """
    Calculate the Coleman-Liau index.
    """
    _ = russian.coleman_liau_index if is_russian else english.coleman_liau_index
    return _(sentences, words, letters)


def overall_index(
    flesch_reading_ease_score: float,
    automated_readability_index: float,
    coleman_liau_index: float,
    *,
    is_russian: bool = False
) -> float:
    """
    Overall indexes value of ``Flesch-Kincaid score``, ``Automated readability`` and ``Coleman-Liau index``.
    """
    _ = russian.overall_index if is_russian else english.overall_index
    return _(flesch_reading_ease_score, automated_readability_index, coleman_liau_index)
