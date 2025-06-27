import os
import json

HISTORY_DIR = "chat_history"

def get_history_path(context):
    """Return the file path for the chat history based on context."""
    os.makedirs(HISTORY_DIR, exist_ok=True)
    return os.path.join(HISTORY_DIR, f"{context}_chat.json")


def save_chat_history(context, history):
    """Save chat history to a local file."""
    try:
        with open(get_history_path(context), "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving chat history: {e}")


def load_chat_history(context):
    """Load chat history from a local file."""
    try:
        path = get_history_path(context)
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading chat history: {e}")
        return []
