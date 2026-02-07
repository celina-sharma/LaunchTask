import json
from pathlib import Path
import pdfplumber
from PIL import Image
import pytesseract
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

PDF_DIR = Path("src/data/raw")
IMAGE_DIR = Path("src/data/images")
METADATA_FILE = IMAGE_DIR / "image_metadata.json"

print("Loading BLIP caption model...")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(DEVICE)

def extract_images_from_pdf(pdf_path: Path):
    pdf_name = pdf_path.stem
    output_dir = IMAGE_DIR / pdf_name
    output_dir.mkdir(parents=True, exist_ok=True)

    image_records = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            if not page.images:
                continue

            for img_idx, img in enumerate(page.images, start=1):
                try:
                    cropped = page.crop(
                        (img["x0"], img["top"], img["x1"], img["bottom"])
                    )

                    image = cropped.to_image(resolution=300)
                    image_name = f"page_{page_num}_img_{img_idx}.png"
                    image_path = output_dir / image_name

                    image.save(image_path)

                    image_records.append(
                        {
                            "image_id": f"{pdf_name}_page_{page_num}_img_{img_idx}",
                            "image_path": str(image_path),
                            "source_pdf": pdf_path.name,
                            "page": page_num,
                        }
                    )
                except Exception as e:
                    print(f"Image extract failed: {e}")

    return image_records


def run_ocr_on_images(metadata):
    for item in metadata:
        try:
            img = Image.open(item["image_path"])
            text = pytesseract.image_to_string(img)
            item["ocr_text"] = text.strip()
        except Exception as e:
            print(f"[WARN] OCR failed for {item['image_path']}: {e}")
            item["ocr_text"] = ""
    return metadata


def generate_captions(metadata):
    print("Generating image captions (BLIP)")

    for item in metadata:
        try:
            image = Image.open(item["image_path"]).convert("RGB")
            inputs = processor(image, return_tensors="pt").to(DEVICE)

            out = model.generate(**inputs, max_new_tokens=50)
            caption = processor.decode(out[0], skip_special_tokens=True)

            item["caption"] = caption.strip()
        except Exception as e:
            print(f"[WARN] Captioning failed for {item['image_path']}: {e}")
            item["caption"] = ""

    return metadata


def main():
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    all_metadata = []

    #image extraction
    for pdf_file in PDF_DIR.glob("*.pdf"):
        print(f"[INFO] Processing PDF: {pdf_file.name}")
        records = extract_images_from_pdf(pdf_file)
        all_metadata.extend(records)

    print(f"Total images extracted: {len(all_metadata)}")

    print("Running OCR")
    all_metadata = run_ocr_on_images(all_metadata)

    #captioning
    all_metadata = generate_captions(all_metadata)

    #save metadata
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(all_metadata, f, indent=2)

    print(f"Image pipeline completed for {len(all_metadata)} images")
    print(f"Metadata saved to {METADATA_FILE}")


if __name__ == "__main__":
    main()
