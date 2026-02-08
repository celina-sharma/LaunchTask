# src/memory/memory_store.py

import json
from datetime import datetime
from pathlib import Path

CHAT_LOG_FILE = Path("CHAT-LOGS.json")


def load_logs():
    if not CHAT_LOG_FILE.exists():
        return []
    with open(CHAT_LOG_FILE, "r") as f:
        return json.load(f)


def save_logs(logs):
    with open(CHAT_LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def save_interaction(endpoint, question, answer, confidence):
    logs = load_logs()

    logs.append({
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "question": question,
        "answer": answer,
        "confidence": confidence
    })

    # keep only last 5
    logs = logs[-5:]

    save_logs(logs)


def get_recent_memory(k=5):
    logs = load_logs()
    return logs[-k:]
