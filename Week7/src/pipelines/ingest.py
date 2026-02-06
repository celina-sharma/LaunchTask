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


def clean_text(text):
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text):
    enc = tiktoken.get_encoding(ENCODING)
    tokens = enc.encode(text)

    chunks = []
    start = 0
    chunk_id = 0

    while start < len(tokens):
        end = start + CHUNK_SIZE
        chunk_tokens = tokens[start:end]

        chunks.append({
            "chunk_id": chunk_id,
            "text": enc.decode(chunk_tokens)
        })

        chunk_id += 1
        next_start = end - CHUNK_OVERLAP
        if next_start <= start:
            break
        start = next_start

    return chunks


def extract_pdf_text(pdf_path):
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                full_text += f"\n[PAGE {page_num + 1}]\n{page_text}"

    return clean_text(full_text)


def main():
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    for pdf in PDF_DIR.glob("*.pdf"):
        print(f"[INFO] Processing {pdf.name}")
        text = extract_pdf_text(pdf)
        chunks = chunk_text(text)

        for c in chunks:
            c["metadata"] = {
                "source": pdf.name
            }

        out_file = CHUNKS_DIR / f"chunks_{pdf.stem}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2)

        print(f"[✓] {len(chunks)} chunks saved → {out_file}")


if __name__ == "__main__":
    main()
