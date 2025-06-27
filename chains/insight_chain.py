from config.settings import GROQ_API_KEY
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from chains.llms import GroqChatLLM

def generate_autonomous_insights(columns, rows):
    prompt = ChatPromptTemplate.from_template(
        """
You are an autonomous data scientist.

You are analyzing a dataset with:
- Columns: {columns}
- Sample Data: {rows}

Task:
1. Think of the most important 5–7 aspects to analyze.
2. Derive 8–10 insights based on patterns in the data.
3. Include numeric patterns, time trends, outliers, correlations, or clusters.
4. Do not include code. Use bullet points and markdown formatting.

Output only insights. Do not explain the prompt.
"""
    )

    formatted = prompt.format_messages(
        columns=", ".join(columns),
        rows=rows[:5]
    )

    llm = GroqChatLLM()
    response = llm(formatted)

    return response.content.strip()
