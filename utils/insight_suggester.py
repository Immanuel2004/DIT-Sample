import json
from utils.groq_handler import call_groq_model  

def suggest_insight_options_explained(csv_data, model_source="groq"):
    """
    Uses LLM to suggest 5 meaningful data insights based on CSV data.
    Returns a list of dictionaries with 'title' and 'description'.
    """
    prompt = f"""
You are a data insights assistant.

Given a dataset in CSV format, generate 5 helpful insights a data analyst might explore.

Respond in valid JSON format as a list like this:
[
  {{
    "title": "Insight Title",
    "description": "What this insight reveals and why it's useful"
  }},
  ...
]

Here is the dataset:
{csv_data[:2000]}
"""

    try:
        raw_response = call_groq_model(prompt)  
        
        if "```json" in raw_response:
            content = raw_response.split("```json")[-1].split("```")[0].strip()
        elif "```" in raw_response:
            content = raw_response.split("```")[1].strip()
        else:
            content = raw_response.strip()

        suggestions = json.loads(content)

        if isinstance(suggestions, list) and all("title" in i and "description" in i for i in suggestions):
            return suggestions
        else:
            raise ValueError("Invalid insight format")

    except Exception as e:
        print("Failed to parse insight suggestions:", e)
        return []
