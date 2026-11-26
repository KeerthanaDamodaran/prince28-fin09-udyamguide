from pathlib import Path

from udyamguide.ingest.parse import (
    ParseError,
    parse_pdf_pymupdf,
    parse_pdf_pypdf,
)


def get_stats(doc):
    return {
        "pages": len(doc.pages),
        "characters": sum(len(p.text) for p in doc.pages),
        "tables": sum(p.tables for p in doc.pages),
        "headings": sum(
            1 for p in doc.pages for line in p.text.splitlines() if line.startswith("#")
        ),
    }


def main():
    files = sorted(Path("data/raw").rglob("*.pdf"))

    print(f"PDF files found: {len(files)}")
    print("-" * 100)
    print(f"{'FILE':45} {'PARSER':10} {'PAGES':8} {'CHARS':10} {'TABLES':8} {'STATUS'}")
    print("-" * 100)

    for path in files:
        for name, parser in [
            ("PyMuPDF", parse_pdf_pymupdf),
            ("pypdf", parse_pdf_pypdf),
        ]:
            try:
                doc = parser(path)
                stats = get_stats(doc)

                print(
                    f"{path.name[:43]:45} {name:10} "
                    f"{stats['pages']:<8} "
                    f"{stats['characters']:<10} "
                    f"{stats['tables']:<8} OK"
                )

            except ParseError as error:
                print(f"{path.name[:43]:45} {name:10} -        -          -        {error.reason}")

    print("-" * 100)


if __name__ == "__main__":
    main()
