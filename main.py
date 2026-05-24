"""Command-line entrypoint for the PDF Reader project.

Usage:
  - `python3 main.py traversal` : recursively extract text from PDFs in
    the `content/` directory (writes per-folder `output.txt`).
  - `python3 main.py page <path> <page_number>` : extract a single
    1-based page from the PDF at `path` and write to `output.txt`.
"""

from pathlib import Path
import sys
from features.traversal import traversal
from features.page import page


def main() -> None:
    """Dispatch CLI subcommands to feature handlers.

    The function reads `sys.argv` to determine the requested feature:
    - `traversal`: runs the `traversal()` feature against the
      `content/` directory next to this script.
    - `page`: expects two additional arguments: a relative `path` to a
      PDF file and a 1-based `page_number` (integer).

    The function performs basic argument validation and prints usage
    errors before exiting with a non-zero status when arguments are
    missing or invalid.

    Returns:
        None
    """

    if len(sys.argv) > 1:
        feature = sys.argv[1].lower()
        script_dir = Path(__file__).parent
        if feature == "traversal":
            folder = script_dir / "content"
            traversal(folder)
        elif feature == "page":
            if len(sys.argv) < 4:
                print("Usage: python3 main.py <mode> <path> <page_number>")
                sys.exit(1)
            try:
                page_number = int(sys.argv[3])
            except ValueError:
                print("Error: page_number must be an integer.")
                sys.exit(1)
            if page_number < 1:
                print("Error: page_number must be a positive integer.")
                sys.exit(1)
            path = script_dir / Path(sys.argv[2])
            page(path, page_number)


if __name__ == "__main__":
    # The guard should be at the bottom of the module so all functions
    # and helpers are defined before the script-run logic executes.
    main()
