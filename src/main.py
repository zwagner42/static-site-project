import sys
from ctypes import ArgumentError
from pathlib import Path

from copystatic import static_to_docs, static_to_public
from generatepage import generate_pages_recursive


def main():
    base_path: str
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"

    static_to_docs()

    generate_pages_recursive(Path("content"), Path("template.html"), Path("docs"), Path(base_path))

main()
