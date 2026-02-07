# Multimodal RAG — Week 7 (Day 3)

## Overview

This module extends the Retrieval-Augmented Generation (RAG) pipeline to support
**multimodal data**, specifically **images embedded inside PDFs**.

The goal of Day-3 is **multimodal ingestion and retrieval**.
All outputs are deterministic, and traceable.

---

## Multimodal Capabilities

After completing Day-3, the system supports the following query modes:

### ✔ Text → Image
Example:
> “Show diagrams related to credit underwriting risk”

- Text query is embedded using CLIP text encoder
- Compared against stored image embeddings
- Top-k visually relevant images are returned

---

### ✔ Image → Image
Example:
> “Find diagrams similar to this one”

- Query image is encoded using CLIP image encoder
- Cosine similarity is used against stored image embeddings
- Similar images from PDFs are ranked and returned

---

### ✔ Image → Text (Context Extraction)
Example:
> “What does this image contain?”

This is handled **without using an LLM**, using:
- OCR text (Tesseract)
- Image captions (BLIP)
- Source metadata (PDF name + page)

The system exposes image-associated textual context, which can later be consumed by an LLM.

---

## Architecture Overview
PDFs
├── Image Extraction
│ └── PNG images
│
├── OCR (Tesseract)
│ └── Extracted text
│
├── Captioning (BLIP)
│ └── Image descriptions
│
├── CLIP Embeddings
│ ├── Image embeddings
│ └── Text embeddings
│
└── Multimodal Retrieval
├── Text → Image
├── Image → Image
└── Image → Text 



---

## Models Used

| Purpose | Model |
|------|------|
Image & Text Embeddings | `openai/clip-vit-base-patch32` |
OCR | Tesseract |
Image Captioning | BLIP |

---

## Vector Index Design

- Image and text embeddings are stored together with metadata
- Cosine similarity is used for retrieval
- This forms a **multimodal vector index**


---

## CLI Demonstrations

### Image → Image Retrieval
```bash
PYTHONPATH=src python test_image.py

Image to text (ocr+caption)
PYTHONPATH=src python test_image_to_text.py --index 7



