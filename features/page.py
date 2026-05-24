"""Page feature: extract a page from a PDF and write the text.

This module provides `page(path, page_number)` which extracts text from a
single 1-based page number of a PDF and writes the result to
`output.txt` in the same directory as the source file.
"""

from pathlib import Path

from utils.pdf_utility import process_pdf_file, write_output


def page(path: Path, page_number: int) -> None:
    """Extract text from a single page of a PDF and write to output.

    Args:
        path: Path-like object pointing to the PDF file.
        page_number: 1-based page number to extract.

    The extracted text is written to `output.txt` in the same directory
    as `path`. If no text is extracted the function prints a message and
    returns without writing.
    """

    print(f"Path: {path}, Page number: {page_number}")
    extracted_text = process_pdf_file(path, page_number)
    if not extracted_text:
        print(f"No text extracted from page {page_number}.")
        return
    write_output(extracted_text, path.parent / "output.txt")