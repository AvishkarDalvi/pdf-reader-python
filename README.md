# PDF Reader

A Python tool to extract text from PDFs, apply regex pattern matching, store questions in a MySQL database, and retrieve them by chapter.

## What it does
- Recursively traverses the `content/` directory and processes any `.pdf` files it finds.
- For each folder that contains one or more PDFs, the script creates `output.txt` in that folder containing the concatenated extracted text from the PDFs in that folder.
- Applies configurable regex patterns to extracted text to parse and extract structured data (e.g., exam questions).
- Stores extracted questions in a MySQL database with subject, chapter, question text, multiple-choice options, and answer.
- Retrieves and displays questions from the database filtered by chapter name.

## Requirements
- Python 3.7+
- pypdf — for PDF text extraction
- mysql-connector-python — for database storage and retrieval

Install dependencies:

```bash
python3 -m pip install --user pypdf mysql-connector-python
```

## Configuration
Create a `config/config.txt` file with the following key-value pairs (one per line):

```
db_host=localhost
db_user=your_mysql_user
db_password=your_mysql_password
db_name=your_database_name
regex=your_regex_pattern_here
```

The `regex` pattern is used to extract structured data (e.g., exam questions) from the PDF text. The pattern should capture question blocks matching your PDF format.

## Usage
Place PDFs under the project (or use an explicit path for the `page` mode). Three CLI modes are available:

### 1. Traversal mode (process a content tree and store in database):

```bash
python3 main.py traversal
```

This looks for a `content/` folder next to `main.py`, recursively extracts text from all `.pdf` files, applies the regex pattern from `config.txt`, parses matching blocks as questions, stores them in the MySQL database, and writes an `output.txt` into each folder that contains PDFs.

### 2. Page mode (extract a single page from a PDF):

```bash
python3 main.py page <relative-or-absolute-pdf-path> <page_number>
```

Example:

```bash
python3 main.py page content/Chemistry\ Questions.pdf 2
```

Extracts text from a single 1-based page number and writes it to `output.txt` in the same directory as the PDF.

### 3. Chapter mode (retrieve questions from the database by chapter):

```bash
python3 main.py chapter <chapter_name>
```

Example:

```bash
python3 main.py chapter "Chapter 1: Basic concepts of chemistry"
```

Queries the database for all questions matching the given chapter name and prints them to the console with options and answers.

## Error handling
- If a PDF file cannot be read the script prints a warning for that page or file and continues where possible.
- If a required PDF path is missing or a critical I/O error occurs (e.g., writing `output.txt` fails), the script prints an error and exits with a non-zero status.

## Implementation details
- Entry point: `main.py` — dispatches `traversal()`, `page()`, or `chapter()` based on CLI arguments.
- PDF extraction: `utils/pdf_utility.py` uses `pypdf.PdfReader` to extract text from PDF files.
- Configuration: `utils/config_utility.py` loads regex patterns and database settings from `config/config.txt`.
- Regex matching: `utils/config_utility.apply_regex()` applies the configured regex pattern to extract question blocks.
- Database: `utils/db_utility.py` manages MySQL connections, creates the `questions` table, and handles inserts/queries.
- Features:
  - `features/traversal.py` — recursively processes PDF directories.
  - `features/page.py` — extracts a single page from a PDF.
  - `features/chapter.py` — retrieves and displays questions by chapter from the database.
- The code writes UTF-8 `output.txt` files and prints progress messages to stdout.

## Possible improvements
- Create the `content/` folder automatically if it does not exist.
- Validate `config.txt` entries and provide helpful error messages if any are missing.
- Add logging instead of printing, with verbosity levels and optional log file output.
- Add OCR fallback (e.g., Tesseract) for scanned PDFs with no extractable text.
- Add a `requirements.txt` or `pyproject.toml` to pin dependency versions.
- Add CLI options to specify custom input directories, output file naming, or regex patterns.
- Implement database migrations or schema versioning for future schema changes.
- Add a web UI or REST API to query and manage questions without CLI.
- Add bulk import/export functionality (CSV, JSON formats).

## Quick checklist
1. Install dependencies: `python3 -m pip install --user pypdf mysql-connector-python`
2. Set up MySQL database and ensure it is running.
3. Create `config/config.txt` with your database credentials and regex pattern.
4. Place PDFs in `content/` (or subfolders).
5. Run `python3 main.py traversal` to extract and store questions, or `python3 main.py chapter "Chapter Name"` to retrieve them.
6. Look for `output.txt` files in any folder that contained PDFs.

If you'd like, I can help you add CLI options, improve error handling, or add a `requirements.txt` file next.

## Notes
- The `traversal` command expects a `content/` directory next to `main.py` (the script does not auto-create it yet).
- The `page` command accepts a path to any PDF file; `page_number` is 1-based and must be a positive integer.
- Each folder that directly contains PDFs will get its own `output.txt` file with the concatenated extracted text for PDFs in that folder. Subfolders that contain PDFs will receive their own `output.txt` files.
- The regex pattern in `config.txt` should match blocks that represent individual questions; each match is parsed and stored as a question record.
- The `chapter` command displays questions from the database and requires that data has been extracted and stored via `traversal` or `page` mode first.
