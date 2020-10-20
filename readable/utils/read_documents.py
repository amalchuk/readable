from os import PathLike
from os import linesep as separator
from pathlib import Path
from typing import Callable, Iterator, Optional

import docx.api as docx
import fitz.fitz as pdf

from readable.utils.decorators import no_exception


def microsoft_word_document(filename: PathLike) -> Iterator[str]:
    document = docx.Document(filename)

    for paragraph in document.paragraphs:
        if (text := paragraph.text.strip()):
            yield text


def pdf_document(filename: PathLike) -> Iterator[str]:
    document = pdf.Document(filename)

    for page in document:
        if (text := page.getText().strip()):
            yield text


def text_document(filename: PathLike) -> Iterator[str]:
    if not isinstance(filename, Path):
        filename = Path(filename)

    with filename.open(encoding="utf-8") as istream:
        for text in istream.readlines():
            if (text := text.strip()):
                yield text


def read_document(filename: PathLike) -> Optional[str]:
    @no_exception(Exception, default=None)
    def callback(user_function: Callable[[PathLike], Iterator[str]]) -> str:
        return separator.join(user_function(filename))

    return callback(microsoft_word_document) or callback(pdf_document) or callback(text_document)
