import json
import os

def load_jsonl(filepath):
    samples = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                samples.append(json.loads(line))
    print(f"Loaded {len(samples)} samples from {filepath}")
    return samples

def remove_empty_outputs(samples):
    cleaned = [s for s in samples if s.get("output", "").strip()]
    removed = len(samples) - len(cleaned)
    print(f"Removed {removed} samples with empty outputs")
    return cleaned


def remove_duplicates(samples):
    seen = set()
    cleaned = []
    for s in samples:
        key = s["instruction"].strip().lower()
        if key not in seen:
            seen.add(key)
            cleaned.append(s)
    removed = len(samples) - len(cleaned)
    print(f"Removed {removed} duplicate instructions")
    return cleaned


def remove_short_outputs(samples, min_words=3):
    cleaned = [s for s in samples if len(s["output"].split()) >= min_words]
    removed = len(samples) - len(cleaned)
    print(f"Removed {removed} samples with less than {min_words} words in output")
    return cleaned


def clean_file(input_path, output_path):
    print(f"\nCleaning: {input_path}")
    samples = load_jsonl(input_path)
    samples = remove_empty_outputs(samples)
    samples = remove_duplicates(samples)
    samples = remove_short_outputs(samples)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        for s in samples:
            f.write(json.dumps(s) + "\n")
    
    print(f"Saved {len(samples)} clean samples to {output_path}")
    return samples


if __name__ == "__main__":
    clean_file("data/train.jsonl", "data/train.jsonl")
    clean_file("data/val.jsonl", "data/val.jsonl")
    print("\nCleaning complete!")