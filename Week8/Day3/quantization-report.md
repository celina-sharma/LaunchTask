# Quantisation Report
## Week 8 — Day 3

---

## What I Did

I took the fine-tuned TinyLlama model from Day 2, merged it with 
the LoRA adapters, and then converted it into 3 different formats 
— INT8, INT4 and GGUF — to compare size, speed and quality.

---

## Model Used
- Base Model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
- Adapters: LoRA adapters from Day 2 fine-tuning
- Libraries: BitsAndBytes, llama.cpp, transformers, peft

---

## Steps Performed

1. Loaded TinyLlama in FP16
2. Loaded LoRA adapters from Day 2
3. Merged base model + adapters into one FP16 model
4. Converted merged model to INT8, INT4 and GGUF
5. Benchmarked all formats

---

## Benchmark Results

| Format | Size | Speed | Quality |
|--------|------|-------|---------|
| FP16 | 2.05 GB | 62.91 t/s | Good |
| INT8 | 1.15 GB | 16.45 t/s | Good |
| INT4 | 0.76 GB | 38.88 t/s | Good |
| GGUF | 1.09 GB | 4.93 t/s | Good |

---

## Size Reduction

| Format | Size | Reduction from FP16 |
|--------|------|---------------------|
| FP16 | 2.05 GB | baseline |
| INT8 | 1.15 GB | 44% smaller |
| INT4 | 0.76 GB | 63% smaller |
| GGUF | 1.09 GB | 47% smaller |

---

## Quality Comparison

All models were tested with the same prompt:
> "Write Python code only, no explanation: def add_two_numbers(a, b):"

**FP16** — Correct function with comments and proper example usage.
No hallucinations. Best quality output.

**INT8** — Correct function with comments and example usage.
Good quality, similar to FP16.

**INT4** — Correct function but minimal output.
Fastest speed but least detailed output.

**GGUF** — Correct function with comments and example usage.
Slight repetition in output but mathematically correct.

---

## Key Observations

- INT4 is the smallest format — 63% smaller than FP16
- FP16 produces the best quality output
- INT4 is fastest on GPU at 38.88 tokens/sec
- GGUF is slowest because it runs differently from bitsandbytes models
- Quality is maintained across all formats — no hallucinations
- GGUF is best for CPU deployment — no GPU needed

---

## Deliverables

- quantized/model-int8
- quantized/model-int4
- quantized/model.gguf
- QUANTISATION-REPORT.md