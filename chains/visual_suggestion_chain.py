from langchain.prompts import ChatPromptTemplate
from chains.llms import GroqChatLLM

def suggest_visualizations(csv_data: str):
    prompt = ChatPromptTemplate.from_template("""
You are a data visualization assistant.

Below is a CSV dataset:

{csv_data}

Based on this data, suggest 3 visualization ideas. For each idea, provide:
- Title
- Description
- Chart type (bar, line, pie, scatter, etc.)
- X-axis column
- Y-axis column (if applicable)

Return your suggestions as a list of dictionaries with keys: title, description, chart_type, x, y (if needed).

Ensure chart_type is one of: ["bar", "line", "scatter", "histogram", "pie"]
""")

    formatted_prompt = prompt.format_messages(csv_data=csv_data[:4000])
    
    llm = GroqChatLLM()
    response = llm(formatted_prompt)
    text = response.content.strip()

    try:
        suggestions = eval(text) if text.startswith("[") else []
        return suggestions
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {e}\n{text}")
