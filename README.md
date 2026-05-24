# PDF Reader

Small script to extract text from PDFs placed in the `content/` folder (including subfolders).

## What it does
- Recursively traverses the `content/` directory and processes any `.pdf` files it finds.
- For each folder that contains one or more PDFs, the script creates `output.txt` in that folder containing the concatenated extracted text from the PDFs in that folder.

## Requirements
- Python 3.7+
- pypdf

Install dependency:

```bash
python3 -m pip install --user pypdf
```

## Usage
Place PDFs under the project (or use an explicit path for the `page` mode). Two CLI modes are available:

- Traversal mode (process a content tree):

```bash
python3 main.py traversal
```

This looks for a `content/` folder next to `main.py`, recursively extracts text from all `.pdf` files, and writes an `output.txt` into each folder that contains PDFs.

- Page mode (extract a single page from a PDF):

```bash
python3 main.py page <relative-or-absolute-pdf-path> <page_number>
```

Example:

```bash
python3 main.py page content/Chemistry\ Questions.pdf 2
```

Notes:
- The `traversal` command expects a `content/` directory next to `main.py` (the script does not auto-create it yet).
- The `page` command accepts a path to any PDF file; `page_number` is 1-based and must be a positive integer.
- Each folder that directly contains PDFs will get its own `output.txt` file with the concatenated extracted text for PDFs in that folder. Subfolders that contain PDFs will receive their own `output.txt` files.

## Error handling
- If a PDF file cannot be read the script prints a warning for that page or file and continues where possible.
- If a required PDF path is missing or a critical I/O error occurs (e.g., writing `output.txt` fails), the script prints an error and exits with a non-zero status.

## Implementation details
- Entry point: `main.py` — it calls `traversal()` on the `content` directory and uses `pypdf.PdfReader` to extract text.
- The code writes UTF-8 `output.txt` files and prints progress messages to stdout.

## Possible improvements
- Create the `content/` folder automatically if it does not exist.
- Add CLI arguments to specify input directory, output file naming, or a single combined output.
- Add logging instead of printing, and add verbosity levels.
- Add OCR fallback (e.g., Tesseract) for scanned PDFs with no extractable text.
- Add a `requirements.txt` or `pyproject.toml` to pin dependencies.

## Quick checklist
- Place PDFs in `content/` (or subfolders).
- Run `python3 main.py` from the project root.
- Look for `output.txt` in any folder that contained PDFs.

If you'd like, I can update the script to create the `content/` folder automatically or add CLI options next.
