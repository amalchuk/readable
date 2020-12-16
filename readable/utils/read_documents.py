from logging import getLogger as get_logger
from pathlib import Path as _P
from typing import Callable, Dict, Iterator, Optional

from docx import Document as DOCXDocument
from docx.document import Document as DOCXElement
from fitz import Document as PDFDocument
from fitz import TEXT_INHIBIT_SPACES

__all__ = ["microsoft_word_document", "pdf_document", "read_document", "text_document"]

logger = get_logger(__name__)


def microsoft_word_document(filename: _P) -> Iterator[str]:
    document: DOCXElement = DOCXDocument(filename)
    for paragraph in document.paragraphs:
        yield paragraph.text.strip()


def pdf_document(filename: _P) -> Iterator[str]:
    document = PDFDocument(filename)
    for page in document:
        yield page.getText("text", flags=TEXT_INHIBIT_SPACES).strip()


def text_document(filename: _P) -> Iterator[str]:
    with filename.open(encoding="utf-8") as istream:
        while text := istream.read(4096):
            yield text.strip()


def read_document(filename: _P) -> Optional[str]:
    allowed_functions: Dict[str, Callable[[_P], Iterator[str]]] = {
        ".docx": microsoft_word_document,
        ".pdf": pdf_document,
        ".txt": text_document
    }
    try:
        extension = filename.suffix.lower()
        callback = allowed_functions[extension]
        return "\n".join(callback(filename))

    except Exception as exception:
        logger.exception(exception)
        return None
