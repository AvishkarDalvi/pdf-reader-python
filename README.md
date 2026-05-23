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
1. Place one or more PDF files inside the `content/` folder (you may also organize PDFs in subfolders).
2. Run the script from the project root:

```bash
python3 main.py
```

Behavior notes:
- The script does not currently create the `content/` folder automatically — the folder must exist before running.
- Each folder that directly contains PDF files will get an `output.txt` file with the extracted text for PDFs in that folder. Subfolders that contain PDFs will receive their own `output.txt` files.

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
