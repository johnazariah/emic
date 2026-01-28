#!/usr/bin/env python3
"""Extract PDF to markdown with proper formatting.

Usage: python extract_pdf.py <pdf_path> [--output-dir <dir>]
"""

import re
import subprocess
import sys
from pathlib import Path


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract text from PDF using pdftotext."""
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True,
        text=True,
    )
    return result.stdout


def get_pdf_info(pdf_path: Path) -> dict:
    """Get PDF metadata."""
    result = subprocess.run(
        ["pdfinfo", str(pdf_path)],
        capture_output=True,
        text=True,
    )
    info = {}
    for line in result.stdout.split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            info[key.strip()] = value.strip()
    return info


def clean_text(text: str) -> str:
    """Clean up extracted text."""
    # Remove excessive blank lines
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    # Fix common OCR/extraction issues
    text = re.sub(r"ﬁ", "fi", text)
    text = re.sub(r"ﬂ", "fl", text)
    text = re.sub(r"ﬀ", "ff", text)
    return text


def format_as_markdown(text: str, info: dict, pdf_name: str) -> str:
    """Format extracted text as markdown."""
    title = info.get("Title", pdf_name.replace("_", " ").replace("-", " "))
    author = info.get("Author", "Unknown")
    pages = info.get("Pages", "?")

    header = f"""# {title}

**Source:** {pdf_name}
**Author:** {author}
**Pages:** {pages}

---

## Full Text

"""
    return header + clean_text(text)


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <pdf_path>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"Error: {pdf_path} not found")
        sys.exit(1)

    # Create output directory
    output_dir = pdf_path.parent / pdf_path.stem.replace(" ", "_")
    output_dir.mkdir(exist_ok=True)

    # Extract and format
    text = extract_pdf_text(pdf_path)
    info = get_pdf_info(pdf_path)
    markdown = format_as_markdown(text, info, pdf_path.stem)

    # Write output
    output_file = output_dir / f"{pdf_path.stem.replace(' ', '_')}_full.md"
    output_file.write_text(markdown)
    print(f"Extracted to: {output_file}")
    print(f"Lines: {len(markdown.splitlines())}")


if __name__ == "__main__":
    main()
