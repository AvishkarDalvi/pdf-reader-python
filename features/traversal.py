"""Directory traversal for extracting text from PDFs.

This module provides a simple recursive traversal that finds PDF files
under a given directory, extracts their text, and writes a single
`output.txt` file into each directory that directly contains one or
more PDFs. Subdirectories are handled recursively and produce their own
`output.txt` files when they contain PDFs.

Behavior notes:
- Non-directory inputs are ignored (the function prints a message and
    returns).
- Extraction uses utilities in `utils.pdf_utility`; extraction errors
    for individual pages are logged and do not abort traversal.
"""

from pathlib import Path

from utils.pdf_utility import process_pdf_file, write_output


def traversal(folder: Path) -> None:
    """Recursively traverse `folder`, extract PDF text, and write output.

    For each directory, this function concatenates extracted text from
    PDF files that are directly inside the directory and writes the
    combined text to `output.txt` in the same directory.

    Args:
        folder: Directory path to traverse. If `folder` is not a
            directory the function prints a message and returns.

    Side effects:
        - Prints progress and error messages to stdout.
        - Creates/overwrites `output.txt` files in directories that
          contain PDFs.

    Returns:
        None
    """

    if not folder.is_dir():
        print(f"Provided path '{folder}' is not a directory.")
        return
    
    extracted_text = ""
    for item in folder.iterdir():
        if item.is_file() and item.suffix.lower() == ".pdf":
            print(f"File: {item.name}")
            extracted_text += process_pdf_file(item)
        elif item.is_dir():
            print(f"Directory: {item.name}")
            traversal(item)

    if not extracted_text:
        return

    output_path = folder / "output.txt"
    write_output(extracted_text, output_path)
    print("Text extracted successfully.")