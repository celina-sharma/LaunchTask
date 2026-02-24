# Benchmark Report
## Week 8 — Day 4

---

## What I Did

I tested inference on 3 different models and measured their speed,
latency and accuracy. I also added streaming output, batch inference
and multi-prompt testing.

---

## Models Tested

1. **Base Model** — Original TinyLlama FP16
2. **Fine-tuned Model** — TinyLlama merged with LoRA adapters from Day 2
3. **GGUF Model** — Quantized model from Day 3 using llama.cpp

---

## Benchmark Results

| Model | Tokens/sec | VRAM | Latency | Accuracy |
|-------|-----------|------|---------|----------|
| Base | 10.51 | 4.0 GB | 3.71 sec | Good |
| Fine-tuned | 20.31 | 4.0 GB | 1.92 sec | Best |
| GGUF | 7.33 | N/A | 12.55 sec | Mixed |

---

## Key Observations

- Fine-tuned model is fastest at 20.31 tokens/sec
- Fine-tuned model has lowest latency at 1.92 sec
- GGUF has highest latency because it uses llama.cpp
- Base and Fine-tuned use same VRAM (4.0 GB)
- GGUF doesn't need VRAM — managed by llama.cpp

---

## Streaming Output

Tested streaming output for all 3 models:
- Base and Fine-tuned → used TextStreamer from transformers
- GGUF → used stream=True from llama_cpp
- All models printed tokens one by one successfully

---

## Batch Inference

Tested batch inference with 2 prompts:
1. add_numbers function
2. multiply_numbers function

All 3 models produced correct outputs with no hallucinations.

---

## Multi-prompt Test

Tested all 3 models with 3 different prompts:
1. Reverse a string
2. Find maximum in a list
3. Calculate factorial

Results:
- Base and Fine-tuned → Correct outputs for all 3 prompts
- GGUF → Correct factorial, minor issues with reverse string

---

## Conclusion

- Fine-tuned model is the best overall — fastest and most accurate
- Base model is reliable but slower than fine-tuned
- GGUF is useful for CPU deployment but slower on GPU
- All models handle basic Python code generation well

---

## Deliverables

- benchmarks/results.csv
- inference/test_inference.py
- BENCHMARK-REPORT.md