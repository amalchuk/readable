from logging import getLogger as get_logger
from pathlib import Path
from typing import Callable, Dict, Iterator, Optional

from docx import Document as DOCXDocument
from docx.document import Document as DOCXElement
from docx.text.paragraph import Paragraph as DOCXParagraph
from fitz import Document as PDFDocument
from fitz import Page as PDFPage
from fitz import TEXT_INHIBIT_SPACES

logger = get_logger(__name__)


def microsoft_word_document(filename: Path) -> Iterator[str]:
    try:
        document: DOCXElement = DOCXDocument(filename)
        for paragraph in document.paragraphs:  # type: DOCXParagraph
            yield paragraph.text.strip()

    except Exception as exception:
        logger.exception(exception)


def pdf_document(filename: Path) -> Iterator[str]:
    get_text: Optional[Callable[..., str]] = None
    try:
        document = PDFDocument(filename)
        for page in document:  # type: PDFPage
            if get_text is None:
                get_text = getattr(page, "getText")

            yield get_text("text", flags=TEXT_INHIBIT_SPACES).strip()

    except Exception as exception:
        logger.exception(exception)


def text_document(filename: Path) -> Iterator[str]:
    try:
        with filename.open(encoding="utf-8") as istream:
            while text := istream.read(8192).strip():
                yield text

    except Exception as exception:
        logger.exception(exception)


def read_document(filename: Path) -> Optional[str]:
    allowed_functions: Dict[str, Callable[[Path], Iterator[str]]] = {
        ".docx": microsoft_word_document,
        ".pdf": pdf_document,
        ".txt": text_document
    }
    try:
        callback = allowed_functions[filename.suffix]
        return "\n".join(callback(filename))

    except Exception as exception:
        logger.exception(exception)
        return None
