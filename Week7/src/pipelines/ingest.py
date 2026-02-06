import json
import re
from pathlib import Path

import pdfplumber
import tiktoken

PDF_DIR = Path("src/data/raw")
CHUNKS_DIR = Path("src/data/chunks")

CHUNK_SIZE = 700
CHUNK_OVERLAP = 150
ENCODING = "cl100k_base"
OUTPUT_FILE = CHUNKS_DIR / "chunks.jsonl"

def clean_text(text: str) -> str:
    """
    Cleans extracted PDF text while preserving paragraph structure.
    """
    text = re.sub(r"\n{3,}", "\n\n", text)     # limit excessive newlines
    text = re.sub(r"[ \t]+", " ", text)        # normalize spaces
    return text.strip()


def extract_pdf_text(pdf_path: Path) -> list:
    """
    Extracts text per page from a PDF.
    Returns: List of dicts -> [{page_num, text}]
    """
    pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if not page_text:
                print(f"[WARN] Empty text on page {page_num} → {pdf_path.name}")
                continue

            pages.append({
                "page": page_num,
                "text": clean_text(page_text)
            })

    return pages


def chunk_text(text: str, enc) -> list:
    """
    Token-aware chunking with overlap.
    """
    tokens = enc.encode(text)

    if len(tokens) <= CHUNK_SIZE:
        return [enc.decode(tokens)]

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + CHUNK_SIZE
        chunk_tokens = tokens[start:end]
        chunks.append(enc.decode(chunk_tokens))

        next_start = end - CHUNK_OVERLAP
        if next_start <= start:
            break

        start = next_start

    return chunks


def process_pdf(pdf_path: Path, enc) -> list:
    """
    Converts a PDF into structured chunks with metadata.
    """
    all_chunks = []
    pages = extract_pdf_text(pdf_path)
    chunk_counter = 0

    for page in pages:
        page_chunks = chunk_text(page["text"], enc)

        for text in page_chunks:
            all_chunks.append({
                "chunk_id": f"{pdf_path.stem}_{chunk_counter}",
                "text": text,
                "metadata": {
                    "source": pdf_path.name,
                    "page": page["page"]
                }
            })
            chunk_counter += 1

    return all_chunks


def main():
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    enc = tiktoken.get_encoding(ENCODING)
    total_chunks = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for pdf in sorted(PDF_DIR.glob("*.pdf")):
            print(f"[INFO] Processing → {pdf.name}")

            try:
                chunks = process_pdf(pdf, enc)
            except Exception as e:
                print(f"Failed to process {pdf.name}: {e}")
                continue

            for chunk in chunks:
                f.write(json.dumps(chunk) + "\n")

            print(f"{len(chunks)} chunks extracted from {pdf.name}")
            total_chunks += len(chunks)

    print(f"\nDONE — Total chunks created: {total_chunks}")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
