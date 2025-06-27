from config.settings import GROQ_API_KEY
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class GroqChatLLM(ChatOpenAI):
    def __init__(self, model="llama3-8b-8192", temperature=0.3, **kwargs):
        super().__init__(
            openai_api_base="https://api.groq.com/openai/v1",
            openai_api_key=GROQ_API_KEY,
            model=model,
            temperature=temperature,
            **kwargs
        )

def compare_datasets(df1_cols, df2_cols, df1_rows, df2_rows):
    prompt = ChatPromptTemplate.from_template(
        """You are a professional data scientist.

Compare these two datasets based on their columns and sample data:

**Dataset A**
Columns: {cols1}
Sample Rows: {rows1}

**Dataset B**
Columns: {cols2}
Sample Rows: {rows2}

Write a comparison report:
- Similarities
- Differences
- Common variables
- Structure, patterns, trends

Return in structured markdown format.
"""
    )

    messages = prompt.format_messages(
        cols1=", ".join(df1_cols),
        cols2=", ".join(df2_cols),
        rows1=df1_rows[:5],
        rows2=df2_rows[:5]
    )

    llm = GroqChatLLM()
    response = llm(messages)

    return response.content.strip()
