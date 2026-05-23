import sys
from pathlib import Path
from pypdf import PdfReader
from pypdf.errors import PdfReadError


def load_pdf(pdf_path: Path) -> PdfReader:
    try:
        return PdfReader(pdf_path)
    except PdfReadError as e:
        print(f"Error reading PDF file '{pdf_path}': {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"PDF file not found: '{pdf_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error opening PDF '{pdf_path}': {e}")
        sys.exit(1)


def extract_text_from_reader(reader: PdfReader) -> str:
    extracted_text = ""
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text()
        except Exception as e:
            print(f"Warning: error processing page {i}: {e}")
            continue
        if text:
            extracted_text += text + "\n"
    return extracted_text


def write_output(extracted_text: str, output_path: Path) -> None:
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
    except (PermissionError, OSError) as e:
        print(f"Error writing to file '{output_path}': {e}")
        sys.exit(1)

def traversal(folder: Path) -> None:
    extracted_text = ""
    for item in folder.iterdir():
        if item.is_file() and item.suffix.lower() == ".pdf":
            print(f"File: {item.name}")
            extracted_text +=process_pdf_file(item)
        elif item.is_dir():
            print(f"Directory: {item.name}")
            traversal(item)
    if not extracted_text:
        return
    output_path = folder / "output.txt"
    write_output(extracted_text, output_path)
    print("Text extracted successfully.")

def main() -> None:
    script_dir = Path(__file__).parent
    folder = script_dir / "content"
    traversal(folder)

def process_pdf_file(pdf_path: Path) -> str:
    if not pdf_path.is_file():
        print(f"PDF file '{pdf_path}' does not exist.")
        sys.exit(1)

    reader = load_pdf(pdf_path)
    return extract_text_from_reader(reader)

if __name__ == "__main__":
    main()
