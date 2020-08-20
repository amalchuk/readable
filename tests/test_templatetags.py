from os import linesep as separator

from django.test.testcases import SimpleTestCase as TestCase
from django.utils.translation import gettext_noop as _

from readable.templatetags.meta_tags import create_meta, string_join
from readable.templatetags.string import line_breaks


class TestTemplateTags(TestCase):
    def test_create_meta(self) -> None:
        author: str = create_meta(name="author", content=_("Andrew Malchuk"))
        self.assertEqual(author, "<meta name=\"author\" content=\"Andrew Malchuk\">")

        custom: str = create_meta(name="custom", content=_("custom meta tag"), additional=_("additional"))
        self.assertEqual(custom, "<meta name=\"custom\" content=\"custom meta tag\" additional=\"additional\">")

    def test_string_join(self) -> None:
        by_comma: str = string_join(", ", (_("bounce"), _("release"), _("absolute")))
        self.assertEqual(by_comma, "bounce, release, absolute")

        by_slash: str = string_join(" / ", (_("bounce"), _("release"), _("absolute")))
        self.assertEqual(by_slash, "bounce / release / absolute")

    def test_line_breaks(self) -> None:
        keywords: str = line_breaks((_("bounce"), _("release"), _("absolute")), "prefix_")
        self.assertIn(separator, keywords)
        self.assertEqual(keywords.split(separator), ["prefix_bounce", "prefix_release", "prefix_absolute"])
