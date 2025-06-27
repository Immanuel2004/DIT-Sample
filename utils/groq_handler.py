import os
import requests
from config.settings import GROQ_API_KEY, GROQ_API_URL, DEFAULT_MODEL, DEFAULT_TEMPERATURE

def call_groq_model(system_prompt: str, user_prompt: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": DEFAULT_TEMPERATURE
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Groq API failed: {response.status_code} - {response.text}")

    try:
        content = response.json()["choices"][0]["message"]["content"]
        return content.strip()
    except Exception as e:
        raise Exception(f"Groq response parsing failed: {e}")
