"""PDF utility helpers used across the project.

This module provides small helpers to open PDF files, extract text from a
PdfReader (either a single 1-based page or the whole document), and write
the extracted text to an `output.txt` file. The helpers use simple
printing and `sys.exit` on unrecoverable errors to match the project's
CLI-style behavior.
"""

from pathlib import Path
import sys
from typing import Optional

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from utils.config_utility import apply_regex, load_config
from utils.db_utility import connect_database, create_questions_table, insert_question, close_database

def load_pdf(pdf_path: Path) -> PdfReader:
    """Open a PDF file and return a PdfReader instance.

    Attempts to open `pdf_path` with `pypdf.PdfReader`. On recoverable page
    errors callers should handle exceptions from page operations; this
    function prints an error message and exits the program for I/O or
    library-level failures to keep behavior simple for the script.

    Args:
        pdf_path: Path to the PDF file to open.

    Returns:
        A `PdfReader` instance for the opened file.

    Exits:
        The process exits with a non-zero status on read/open failures.
    """

    try:
        return PdfReader(pdf_path)
    except PdfReadError as e:
        print(f"Error reading PDF file '{pdf_path}': {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"PDF file not found: '{pdf_path}'")
        sys.exit(1)
    except OSError as e:
        print(f"Unexpected OS error opening PDF '{pdf_path}': {e}")
        sys.exit(1)


def extract_text_from_reader(reader: PdfReader, page_number: Optional[int] = None) -> str:
    """Extract text from a PdfReader.

    If `page_number` is None the function extracts text from all pages and
    concatenates them with newline separators. If `page_number` is an
    integer it is treated as a 1-based page index and only that page is
    extracted.

    Args:
        reader: Open `PdfReader` instance.
        page_number: Optional 1-based page number to extract. If `None`,
            extract the whole document.

    Returns:
        Extracted text as a string (may be empty).
    """

    # Extract whole document when no specific page requested
    if page_number is None:
        extracted_text = ""
        for i, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text()
            except (AttributeError, TypeError, ValueError) as e:
                print(f"Warning: error processing page {i}: {e}")
                continue
            if text:
                extracted_text += text + "\n"
        return extracted_text

    # Single-page extraction (1-based index)
    total_pages = len(reader.pages)
    if page_number < 1 or page_number > total_pages:
        print(f"Error: page number {page_number} is out of range (1-{total_pages}).")
        return ""
    try:
        return reader.pages[page_number - 1].extract_text() or ""
    except (AttributeError, TypeError, ValueError) as e:
        print(f"Warning: error processing page {page_number}: {e}")
        return ""


def process_pdf_file(pdf_path: Path, page_number: Optional[int] = None) -> str:
    """Validate a PDF path, open it, and return extracted text.

    Args:
        pdf_path: Path to a PDF file.
        page_number: Optional page number to extract (1-based). If None, extracts all pages.

    Returns:
        The extracted text from the PDF as a string.

    Exits:
        The process exits with a non-zero status if `pdf_path` does not
        point to a regular file.
    """

    if not pdf_path.is_file():
        print(f"PDF file '{pdf_path}' does not exist.")
        sys.exit(1)

    reader = load_pdf(pdf_path)
    extracted_text = extract_text_from_reader(reader, page_number)
    lines = extracted_text.splitlines()
    subject = extract_subject(lines)
    current_chapter = extract_current_chapter(lines)
    regex_matches = []
    regex_config = load_config()
    regex_matches = apply_regex(extracted_text, regex_config)
    connection = connect_database()
    create_questions_table(connection)
    for question_block in regex_matches:
        question = parse_question(subject, current_chapter, question_block)
        insert_question(connection, question)
    close_database(connection)
    return "\n".join(regex_matches)

def parse_question(subject, current_chapter, question_block) -> dict:
    lines = question_block.splitlines()
    parts = lines[0].split(" ", 1)
    question_text = parts[1]
    options = [option.strip() for option in lines[1:5]]
    answer = lines[5].replace("Answer:", "").strip()
    question = {
            "subject": subject,
            "chapter": current_chapter,
            "question": question_text,
            "options": options,
            "answer": answer
        }
    
    return question

def extract_current_chapter(lines):
    current_chapter = None
    for line in lines:
        if line.startswith("Chapter"):
            current_chapter = line.strip()
            break
    return current_chapter

def extract_subject(lines):
    subject = None
    for line in lines:
        if line.strip():
            subject = line.strip()
            break
    return subject


def write_output(extracted_text: str, output_path: Path) -> None:
    """Write `extracted_text` to `output_path` using UTF-8 encoding.

    Args:
        extracted_text: Text to write to disk.
        output_path: Path where the output file will be created/overwritten.

    Exits:
        The process exits with a non-zero status if writing fails due to
        permission or other OS-level errors.
    """

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
    except (PermissionError, OSError) as e:
        print(f"Error writing to file '{output_path}': {e}")
        sys.exit(1)