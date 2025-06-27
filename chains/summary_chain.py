from config.settings import GROQ_API_KEY
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from chains.llms import GroqChatLLM

def generate_summary(columns, sample_rows):
    prompt = ChatPromptTemplate.from_template(
        """
You are a data analyst.

Your job is to analyze and summarize any dataset you're given.

Columns:
{columns}

Sample Rows:
{rows}

Generate a summary that includes:
- What this dataset might be about
- Who might use it and why
- Key patterns or signals you detect
- Unique or surprising insights
- Mention if it's time-based, user-based, geography-based, etc.

Avoid vague descriptions. Be precise and back your claims using column context or row patterns.
"""
    )

    formatted_prompt = prompt.format_messages(
        columns=", ".join(columns),
        rows=sample_rows[:5]
    )

    llm = GroqChatLLM()
    response = llm(formatted_prompt)

    return response.content.strip()
