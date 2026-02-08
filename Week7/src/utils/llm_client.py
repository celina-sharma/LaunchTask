import os
import yaml
from pathlib import Path
from groq import Groq

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "model.yaml"

with open(CONFIG_PATH, "r") as f:
    cfg = yaml.safe_load(f)

PROVIDER = cfg["provider"]
MODEL = cfg["model_name"]
API_KEY = os.getenv(cfg["api_key_env"])


def call_llm(prompt: str) -> str:
    if PROVIDER == "groq":
        return _groq_call(prompt)
    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")


def _groq_call(prompt: str) -> str:
    if not API_KEY:
        raise RuntimeError(
            f"{cfg['api_key_env']} not found. Did you export it?"
        )

    client = Groq(api_key=API_KEY)

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert SQL generator. "
                    "Return ONLY valid SQLite SQL. No markdown. No explanations."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return completion.choices[0].message.content.strip()
