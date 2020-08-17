from django.test.testcases import SimpleTestCase as TestCase

from readable.utils.plain_language import indexes
from readable.utils.plain_language.metrics import compute
from readable.utils.plain_language.processing import sentences, syllables, words


class TestPlainLanguage(TestCase):
    def test_sentences(self) -> None:
        text = "Привет. Это я. Просто хотела узнать, не хотел бы ты встретиться спустя все эти годы."
        first_sentence, second_sentence, third_sentence = sentences(text)
        self.assertEqual(first_sentence, "Привет.")
        self.assertEqual(second_sentence, "Это я.")
        self.assertEqual(third_sentence, "Просто хотела узнать, не хотел бы ты встретиться спустя все эти годы.")

        text = "Hello. It's me. I was wondering if after all these years you'd like to meet."
        first_sentence, second_sentence, third_sentence = sentences(text)
        self.assertEqual(first_sentence, "Hello.")
        self.assertEqual(second_sentence, "It's me.")
        self.assertEqual(third_sentence, "I was wondering if after all these years you'd like to meet.")

    def test_syllables(self) -> None:
        self.assertEqual(syllables("мост"), 1)
        self.assertEqual(syllables("война"), 2)
        self.assertEqual(syllables("зеркальный"), 3)
        self.assertEqual(syllables("масленица"), 4)
        self.assertEqual(syllables("электричество"), 5)
        self.assertEqual(syllables("стихотворение"), 6)

        self.assertEqual(syllables("bounce"), 1)
        self.assertEqual(syllables("release"), 2)
        self.assertEqual(syllables("absolute"), 3)
        self.assertEqual(syllables("entertainment"), 4)
        self.assertEqual(syllables("accommodation"), 5)
        self.assertEqual(syllables("availability"), 6)

    def test_words(self) -> None:
        text = "Привет. Это я. Просто хотела узнать, не хотел бы ты встретиться спустя все эти годы."
        wrapped = list(words(text))
        self.assertEqual(len(wrapped), 15)

        text = "Hello. It's me. I was wondering if after all these years you'd like to meet."
        wrapped = list(words(text))
        self.assertEqual(len(wrapped), 17)

    def test_metrics(self) -> None:
        text = "Привет. Это я. Просто хотела узнать, не хотел бы ты встретиться спустя все эти годы."
        metrics = compute(text)
        self.assertDictEqual(metrics, {"is_russian": True, "sentences": 3, "words": 15, "letters": 66, "syllables": 27})

        text = "Hello. It's me. I was wondering if after all these years you'd like to meet."
        metrics = compute(text)
        self.assertDictEqual(metrics, {"is_russian": False, "sentences": 3, "words": 17, "letters": 57, "syllables": 21})

    def test_indexes(self) -> None:
        # Flesch-Kincaid score:
        value = indexes.flesch_reading_ease_score(sentences=100, words=10000, syllables=2500, is_russian=True)
        self.assertGreaterEqual(value, 76.0)
        self.assertLessEqual(value, 77.0)

        value = indexes.flesch_reading_ease_score(sentences=100, words=10000, syllables=2500, is_russian=False)
        self.assertGreaterEqual(value, 84.0)
        self.assertLessEqual(value, 85.0)

        # Automated readability index:
        value = indexes.automated_readability_index(sentences=100, words=10000, letters=30000, is_russian=True)
        self.assertGreaterEqual(value, 15.0)
        self.assertLessEqual(value, 16.0)

        value = indexes.automated_readability_index(sentences=100, words=10000, letters=30000, is_russian=False)
        self.assertGreaterEqual(value, 42.0)
        self.assertLessEqual(value, 43.0)

        # Coleman-Liau index:
        value = indexes.coleman_liau_index(sentences=100, words=10000, letters=30000, is_russian=True)
        self.assertGreaterEqual(value, 0.0)
        self.assertLessEqual(value, 1.0)

        value = indexes.coleman_liau_index(sentences=100, words=10000, letters=30000, is_russian=False)
        self.assertGreaterEqual(value, 1.0)
        self.assertLessEqual(value, 2.0)

        # Overall indexes value of Flesch-Kincaid score, Automated readability and Coleman-Liau index:
        value = indexes.overall_index(
            flesch_reading_ease_score=90.0,
            automated_readability_index=6.0,
            coleman_liau_index=8.0,
            is_russian=True)
        self.assertGreaterEqual(value, 70.0)
        self.assertLessEqual(value, 80.0)

        value = indexes.overall_index(
            flesch_reading_ease_score=90.0,
            automated_readability_index=6.0,
            coleman_liau_index=8.0,
            is_russian=False)
        self.assertGreaterEqual(value, 60.0)
        self.assertLessEqual(value, 70.0)
