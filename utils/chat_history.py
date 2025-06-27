import os
import json

CHAT_DIR = "chat_logs"
os.makedirs(CHAT_DIR, exist_ok=True)

def get_chat_path(context: str) -> str:
    return os.path.join(CHAT_DIR, f"{context}_chat_history.json")

def load_chat_history(context: str):
    path = get_chat_path(context)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_chat_history(context: str, history: list):
    path = get_chat_path(context)
    try:
        with open(path, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Failed to save chat history: {e}")
