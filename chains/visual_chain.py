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

def generate_visual_suggestions(df):
    column_types = {col: str(dtype) for col, dtype in df.dtypes.items()}
    columns = list(df.columns)
    sample_rows = df.head(5).to_dict(orient="records")

    prompt = ChatPromptTemplate.from_template(
        """
You are a data visualization expert.

You are given:
- Column names: {columns}
- Column data types: {types}
- Sample rows: {rows}

Your job is to:
1. Propose 3 to 5 **clear and useful visualizations** based on this data.
2. Each must include:
   - An insight (e.g., trend, comparison, distribution)
   - A chart type (bar, line, scatter, pie, histogram)
   - What to plot on x-axis and y-axis (or only x for hist/pie)
3. Prefer time, categorical, and numeric fields where appropriate.
4. Avoid repetition and make sure chart types fit the column types.

 Return a valid Python list like:
[
  {
    "insight": "Sales increased month-over-month.",
    "chart": { "type": "line", "x": "month", "y": "sales" }
  },
  ...
]

 DO NOT return markdown or explanations. Just return the list only.
"""
    )

    formatted = prompt.format_messages(
        columns=", ".join(columns),
        types=str(column_types),
        rows=sample_rows
    )

    llm = GroqChatLLM()
    response = llm(formatted)

    try:
        suggestions = eval(response.content.strip())
        if isinstance(suggestions, list):
            return suggestions
    except Exception:
        pass

    return []
