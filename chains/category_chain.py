from config.settings import GROQ_API_KEY
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from chains.llms import GroqChatLLM

def generate_insight_categories(columns, rows):
    prompt = ChatPromptTemplate.from_template(
        """
You are an expert AI data analyst.

Your job is to read the **columns** and **sample rows** from a dataset and propose the most useful insight categories a user should explore.

Dataset Columns:
{columns}

Sample Rows:
{rows}

Based on this data, suggest 5–7 meaningful insight categories (beyond basic stats). 
Return only a **valid Python list of strings**.

 Examples of good categories:
- Time-based Performance Trends
- User Segmentation by Region
- Engagement Drop-off Points
- Feature Usage Patterns
- Behavior by Demographics

 Do NOT include markdown, explanations, or labels.
Just return:
["Category 1", "Category 2", ..., "Category N"]
"""
    )

    try:
        formatted = prompt.format_messages(
            columns=", ".join(columns),
            rows=rows[:5]
        )

        llm = GroqChatLLM()
        response = llm(formatted)

        text = response.content.strip()
        categories = eval(text)

        if isinstance(categories, list) and all(isinstance(cat, str) for cat in categories):
            return categories

    except Exception:
        pass

    return [
        "Performance & Accuracy Insights",
        "Learning Patterns",
        "Demographic Trends",
        "Engagement Analysis",
        "Comparative Performance",
        "Visualization Insights"
    ]
