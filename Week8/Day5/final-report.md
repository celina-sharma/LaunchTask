# Final Report — Week 8: LLM Fine-tuning

## Overview
This week I built a complete LLM pipeline from scratch — from dataset 
preparation to fine-tuning, quantization, benchmarking and deploying 
a local API server.

---

## Day 1 — Dataset Preparation
- Loaded and cleaned CodeAlpaca dataset
- Split into train and validation sets
- Analyzed token distribution and data quality
- Saved as train.jsonl and val.jsonl

## Day 2 — LoRA Fine-tuning
- Loaded TinyLlama 1.1B in 4-bit using BitsAndBytes
- Applied LoRA adapters using PEFT library
- Fine-tuned on CodeAlpaca dataset
- Saved adapters (only 4.5 MB vs 2.2 GB full model)

## Day 3 — Quantization
- Merged base model with LoRA adapters into FP16 model
- Converted to INT8 (44% smaller than FP16)
- Converted to INT4 (63% smaller than FP16)
- Converted to GGUF using llama.cpp (47% smaller than FP16)

## Day 4 — Inference Benchmarking
- Tested all 3 models (Base, Fine-tuned, GGUF)
- Measured tokens/sec, VRAM, latency, accuracy
- Added streaming output, batch inference, multi-prompt test
- Fine-tuned model was fastest at 20.31 tokens/sec

## Day 5 — Local LLM API
- Built FastAPI server with /generate and /chat endpoints
- Built Streamlit UI with Chat and Generate modes
- Added keyword filter for coding/AI questions only
- Added system prompt, temperature, top-k, top-p controls
- Created Dockerfile for containerization

---

## Benchmark Results

| Model | Tokens/sec | VRAM | Latency | Accuracy |
|-------|-----------|------|---------|----------|
| Base | 10.51 | 4.0 GB | 3.71 sec | Good |
| Fine-tuned | 20.31 | 4.0 GB | 1.92 sec | Best |
| GGUF | 7.33 | N/A | 12.55 sec | Mixed |

---

## Key Learnings

1. **LoRA is efficient** — only 4.5 MB of adapters instead of full 2.2 GB model
2. **Quantization saves memory** — INT4 is 63% smaller than FP16
3. **Fine-tuning improves speed** — 2x faster than base model
4. **Small models have limitations** — TinyLlama 1.1B hallucinates on complex tasks
5. **GGUF is best for CPU** — runs without GPU
6. **FastAPI is great for serving** — easy to build production ready APIs

---

## Challenges Faced

- GPU credits running out during quantization
- GGUF tokenizer compatibility issues
- INT4 hallucinations on mathematical tasks
- TinyLlama not strictly following system prompts

---

## Deliverables

### Day 1
- data/train.jsonl
- data/val.jsonl
- dataset-analysis.md

### Day 2
- adapters/
- notebooks/lora_train.ipynb
- training-report.md

### Day 3
- quantized/model-int8/
- quantized/model-int4/
- quantized/model.gguf
- quantization-report.md

### Day 4
- benchmarks/results.csv
- inference/test_inference.py
- benchmark-report.md

### Day 5
- deploy/app.py
- deploy/model_loader.py
- deploy/config.py
- deploy/streamlit_app.py
- README.md
- DOCKERFILE
- FINAL-REPORT.md