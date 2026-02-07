import json
import argparse

IMAGE_DATA_FILE = "src/data/images/image_metadata_with_embeddings.json"


def main(index: int):
    with open(IMAGE_DATA_FILE, "r") as f:
        data = json.load(f)

    if index < 0 or index >= len(data):
        raise ValueError(f"Index must be between 0 and {len(data) - 1}")

    item = data[index]

    print("\nIMAGE → TEXT OUTPUT\n")
    print(f"Source PDF : {item['source_pdf']}")
    print(f"Page       : {item['page']}")
    print(f"Image Path : {item['image_path']}\n")

    print("Caption:")
    print(item.get("caption", "N/A"))

    print("\nOCR Text:")
    print(item.get("ocr_text", "N/A"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Image to text demo using OCR + Caption"
    )
    parser.add_argument(
        "--index",
        type=int,
        default=0,
        help="Index of image in metadata file (default-0)"
    )

    args = parser.parse_args()
    main(args.index)
