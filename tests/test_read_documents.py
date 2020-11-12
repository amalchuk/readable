import logging
from os import urandom
from pathlib import Path as P
from tempfile import mkstemp as temporary_file
from typing import List

from django.test.testcases import SimpleTestCase as TestCase
from docx import Document as DOCXDocument
from reportlab.pdfgen.canvas import Canvas as PDFDocument

from readable.utils.read_documents import microsoft_word_document
from readable.utils.read_documents import pdf_document
from readable.utils.read_documents import read_document
from readable.utils.read_documents import text_document


class TestReadDocuments(TestCase):
    def setUp(self) -> None:
        logging.disable(logging.ERROR)
        self.lorem: List[str] = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Aliquam sollicitudin lorem non hendrerit porttitor.",
            "Donec tincidunt quam ut nibh varius pharetra.",
            "Praesent venenatis metus a elit ullamcorper cursus.",
            "Etiam ullamcorper quam quis turpis accumsan, consequat maximus risus tristique."
        ]

    def test_microsoft_word_document(self) -> None:
        _, tempfile = temporary_file(suffix=".docx")

        document = DOCXDocument()
        for paragraph in self.lorem:
            document.add_paragraph(paragraph)

        document.save(tempfile)
        text = "\n".join(microsoft_word_document(P(tempfile)))
        self.assertEqual(text, "\n".join(self.lorem))

    def test_pdf_document(self) -> None:
        _, tempfile = temporary_file(suffix=".pdf")

        document = PDFDocument(tempfile)
        text_object = document.beginText(100, 100)

        for paragraph in self.lorem:
            text_object.textLine(paragraph)

        document.drawText(text_object)
        document.showPage()
        document.save()

        text = "\n".join(pdf_document(P(tempfile)))
        self.assertEqual(text, "\n".join(self.lorem))

    def test_text_document(self) -> None:
        _, tempfile = temporary_file(suffix=".txt")
        document = P(tempfile)
        document.write_text("\n".join(self.lorem))

        text = "\n".join(text_document(P(tempfile)))
        self.assertEqual(text, "\n".join(self.lorem))

    def test_read_document(self) -> None:
        _, tempfile = temporary_file(suffix=".txt")
        document = P(tempfile)
        document.write_text("\n".join(self.lorem))

        text = read_document(P(tempfile))
        self.assertIsNotNone(text)
        self.assertEqual(text, "\n".join(self.lorem))

        _, tempfile = temporary_file(suffix=".bin")
        document = P(tempfile)
        document.write_bytes(urandom(128))
        self.assertIsNone(read_document(document))

    def tearDown(self) -> None:
        logging.disable(logging.NOTSET)