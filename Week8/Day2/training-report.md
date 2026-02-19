# Training Report
## Week 8 — Day 2 | Parameter-Efficient Fine-Tuning (LoRA/QLoRA)

---

## 1. Overview
This report documents the fine-tuning of TinyLlama 1.1B using QLoRA
on the CodeAlpaca dataset prepared in Day 1.

---

## 2. Model Details

| Property | Details |
|----------|---------|
| Base Model | TinyLlama/TinyLlama-1.1B-Chat-v1.0 |
| Method | QLoRA (4-bit quantization + LoRA) |
| Dataset | CodeAlpaca (1,023 train / 116 val) |

---

## 3. LoRA Configuration

| Parameter | Value |
|-----------|-------|
| Rank (r) | 16 |
| Alpha | 32 |
| Dropout | 0.05 |
| Task Type | CAUSAL_LM |

---

## 4. Training Configuration

| Parameter | Value |
|-----------|-------|
| Epochs | 3 |
| Batch Size | 4 |
| Learning Rate | 2e-4 |
| Quantization | 4-bit (NF4) |

---

## 5. Results

| Metric | Value |
|--------|-------|
| Total Steps | 768 |
| Final Loss | 0.7644 |
| Training Time | 435 seconds |
| Samples/Second | 7.04 |
| Trainable Parameters | 2,252,800 (0.20%) |
| Total Parameters | 1,102,301,184 |

---

## 6. Key Observations
- Loss decreased from ~2.5 to 0.76 showing model learned successfully
- Only 0.20% parameters were trained — rest were frozen 
- 4-bit quantization allowed training on free T4 GPU 
- Adapter weights saved successfully 

---

## 7. Deliverables

| File | Description |
|------|-------------|
| `notebooks/lora_train.ipynb` | Training notebook |
| `adapters/adapter_model.safetensors` | Trained LoRA weights |
| `adapters/adapter_config.json` | LoRA configuration |
| `TRAINING-REPORT.md` | This report |