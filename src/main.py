from pathlib import Path

from copystatic import static_to_public
from generatepage import generate_pages_recursive


def main():
    static_to_public()

    generate_pages_recursive(Path("content"), Path("template.html"), Path("public"))

main()
