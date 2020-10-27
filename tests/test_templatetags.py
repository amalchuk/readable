from django.test.testcases import SimpleTestCase as TestCase
from django.utils.translation import gettext_noop as _

from readable.templatetags.meta_tags import create_meta
from readable.templatetags.meta_tags import string_join


class TestTemplateTags(TestCase):
    def test_create_meta(self) -> None:
        author: str = create_meta(name="author", content=_("Andrew Malchuk"))
        self.assertHTMLEqual(author, "<meta name=\"author\" content=\"Andrew Malchuk\">")

        custom: str = create_meta(name="custom", content=_("custom meta tag"), additional=_("additional"))
        self.assertHTMLEqual(custom, "<meta name=\"custom\" content=\"custom meta tag\" additional=\"additional\">")

    def test_string_join(self) -> None:
        by_comma: str = string_join(", ", (_("bounce"), _("release"), _("absolute")))
        self.assertEqual(by_comma, "bounce, release, absolute")

        by_slash: str = string_join(" / ", (_("bounce"), _("release"), _("absolute")))
        self.assertEqual(by_slash, "bounce / release / absolute")
