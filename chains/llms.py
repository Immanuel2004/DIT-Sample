from langchain_community.chat_models import ChatOpenAI
from config.settings import GROQ_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE

class GroqChatLLM(ChatOpenAI):
    def __init__(self, model=DEFAULT_MODEL, temperature=DEFAULT_TEMPERATURE, **kwargs):
        super().__init__(
            openai_api_base="https://api.groq.com/openai/v1",
            openai_api_key=GROQ_API_KEY,
            model=model,
            temperature=temperature,
            **kwargs
        )
