# PDF Reader

Small script to extract text from a PDF placed in the `content/` folder and write it to `output.txt` in the same folder.

## Requirements
- Python 3.7+
- pypdf

Install dependency:

```bash
python3 -m pip install --user pypdf
```

## Usage
1. Put `Chemistry Questions.pdf` inside the `content/` folder next to this script. The script will create the `content/` folder if it does not exist.
2. Run the script:

```bash
python3 python-projects/pdf-reader/main.py
```

Output: `content/output.txt` will be created (or overwritten) with the extracted text.

## Error handling
- If the `content/` folder cannot be created the script exits with an error message.
- If `Chemistry Questions.pdf` is not found in `content/` the script prints an error and exits.
- If `output.txt` cannot be written (permissions, disk errors) the script prints an error and exits.

## Notes / Improvements
- To process a different PDF or output path, modify `main.py` or add CLI argument parsing.
- Consider adding a `requirements.txt` if you want to pin dependencies.
