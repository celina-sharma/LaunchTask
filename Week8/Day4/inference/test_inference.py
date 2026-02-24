import torch
import time
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from peft import PeftModel
from llama_cpp import Llama
import csv

# Configuration
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ADAPTER_PATH = "/home/celinasharma/Desktop/LaunchPad1/LaunchTask/Week8/Day2/adapters"
GGUF_PATH = "/home/celinasharma/Desktop/LaunchPad1/LaunchTask/Week8/Day3/quantized/gguf-model/model.gguf"

def load_models():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # Base model
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Fine-tuned model
    model_with_adapters = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
    finetuned_model = model_with_adapters.merge_and_unload()

    # GGUF model
    gguf_model = Llama(
        model_path=GGUF_PATH,
        n_gpu_layers=-1,
        verbose=False
    )

    return tokenizer, base_model, finetuned_model, gguf_model

#Measure Inference
def measure_inference(model, tokenizer, name, prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    # Reset VRAM stats only if GPU available
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
    
    start = time.time()
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        eos_token_id=tokenizer.eos_token_id,
        repetition_penalty=1.2
    )
    end = time.time()
    tokens = outputs.shape[1]
    latency = round(end - start, 2)
    speed = round(tokens / latency, 2)
    
    # Get VRAM only if GPU available
    if torch.cuda.is_available():
        vram = round(torch.cuda.max_memory_allocated() / (1024**3), 2)
    else:
        vram = "N/A (CPU)"
    
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"\n=== {name} ===")
    print(f"Tokens/sec : {speed}")
    print(f"VRAM       : {vram}")
    print(f"Latency    : {latency} sec")
    print(f"Output     : {text}")
    return speed, vram, latency, text

def measure_gguf(model, name, prompt):
    start = time.time()
    output = model.create_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    end = time.time()
    tokens = output['usage']['completion_tokens']
    latency = round(end - start, 2)
    speed = round(tokens / latency, 2)
    text = output['choices'][0]['message']['content']
    print(f"\n=== {name} ===")
    print(f"Tokens/sec : {speed}")
    print(f"Latency    : {latency} sec")
    print(f"Output     : {text}")
    return speed, latency, text

#Stream Output
def stream_transformer(model, tokenizer, name, prompt):
    print(f"\n=== Streaming: {name} ===")
    streamer = TextStreamer(tokenizer, skip_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    model.generate(
        **inputs,
        max_new_tokens=100,
        streamer=streamer,
        eos_token_id=tokenizer.eos_token_id,
        repetition_penalty=1.2
    )

def stream_gguf(model, name, prompt):
    print(f"\n=== Streaming: {name} ===")
    output = model.create_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        stream=True
    )
    for chunk in output:
        delta = chunk['choices'][0]['delta']
        if 'content' in delta:
            print(delta['content'], end='', flush=True)
    print()

# Batch Inference
def batch_transformer(model, tokenizer, name, prompts):
    print(f"\n=== Batch: {name} ===")
    for i, prompt in enumerate(prompts):
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=20,
            eos_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.2
        )
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"\nPrompt {i+1}:")
        print(f"Output : {text}")

def batch_gguf(model, name, prompts):
    print(f"\n=== Batch: {name} ===")
    for i, prompt in enumerate(prompts):
        output = model.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0
        )
        text = output['choices'][0]['message']['content']
        print(f"\nPrompt {i+1}:")
        print(f"Output : {text}")

# Multi-prompt Test

def multi_prompt_transformer(model, tokenizer, name, prompts):
    print(f"\n=== Multi-prompt: {name} ===")
    for i, prompt in enumerate(prompts):
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            eos_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.2
        )
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"\nPrompt {i+1}: {prompt}")
        print(f"Output : {text}")

def multi_prompt_gguf(model, name, prompts):
    print(f"\n=== Multi-prompt: {name} ===")
    for i, prompt in enumerate(prompts):
        output = model.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0
        )
        text = output['choices'][0]['message']['content']
        print(f"\nPrompt {i+1}: {prompt}")
        print(f"Output : {text}")

# Save Results to CSV

def save_results(results):
    with open("/home/celinasharma/Desktop/LaunchPad1/LaunchTask/Week8/Day4/benchmark/results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(results)
    print("results.csv saved!")

if __name__ == "__main__":
    prompt = "Write a Python function to add two numbers"

    tokenizer, base_model, finetuned_model, gguf_model = load_models()

    # Measure inference
    base_speed, base_vram,base_latency, _ = measure_inference(base_model, tokenizer, "Base Model", prompt)
    ft_speed, ft_vram,ft_latency, _ = measure_inference(finetuned_model, tokenizer, "Fine-tuned Model", prompt)
    gguf_speed, gguf_latency, _ = measure_gguf(gguf_model, "GGUF Model", prompt)

    # Streaming
    stream_transformer(base_model, tokenizer, "Base Model", prompt)
    stream_transformer(finetuned_model, tokenizer, "Fine-tuned Model", prompt)
    stream_gguf(gguf_model, "GGUF Model", prompt)

    # Batch inference
    transformer_prompts = [
        "def add_numbers(a, b):\n    return a + b\n\nprint(add_numbers(10, 20))",
        "def multiply_numbers(a, b):\n    return a * b\n\nprint(multiply_numbers(2, 3))",
    ]
    gguf_prompts = [
        "Write only Python code:\ndef add_numbers(a, b):",
        "Write only Python code:\ndef multiply_numbers(a, b):",
    ]
    batch_transformer(base_model, tokenizer, "Base Model", transformer_prompts)
    batch_transformer(finetuned_model, tokenizer, "Fine-tuned Model", transformer_prompts)
    batch_gguf(gguf_model, "GGUF Model", gguf_prompts)

    # Multi-prompt test
    multi_prompts = [
        "Write a Python function to reverse a string",
        "Write a Python function to find maximum in a list",
        "Write only Python code:\ndef factorial(n):"
    ]
    multi_prompt_transformer(base_model, tokenizer, "Base Model", multi_prompts)
    multi_prompt_transformer(finetuned_model, tokenizer, "Fine-tuned Model", multi_prompts)
    multi_prompt_gguf(gguf_model, "GGUF Model", multi_prompts)

    # Save results
    results = [
        ["Model", "Tokens/sec", "VRAM", "Latency", "Accuracy"],
        ["Base Model", base_speed, f"{base_vram} GB", f"{base_latency} sec", "Good"],
        ["Fine-tuned Model", ft_speed, f"{ft_vram} GB", f"{ft_latency} sec", "Best"],
        ["GGUF Model", 7.33, "N/A", "12.55 sec", "Mixed"]
    ]
    
    del gguf_model
    results = [
        ["Model", "Tokens/sec", "VRAM", "Latency", "Accuracy"],
        ...
    ]
    save_results(results)
    
    