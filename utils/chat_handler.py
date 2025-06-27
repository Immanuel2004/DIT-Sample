import json
from .groq_handler import call_groq_model
from .logger import logger

def handle_user_query_dynamic(user_query, df, model_source="groq"):
    schema = ", ".join(df.columns.tolist())
    preview = df.head(3).to_dict(orient='records')

    system_prompt = """
You are a helpful, friendly, and human-like data analyst assistant.

Your job is to clearly and simply answer any question related to the dataset provided below. Use natural, markdown-friendly language that’s easy for anyone to understand — like you're chatting with a colleague, not writing code.

Avoid technical jargon, programming syntax, or overly complex stats. Use everyday language and short sentences.

For chart requests, respond ONLY like this:
{
  "response": {
    "chart_type": "bar",
    "group_by": ["column1", "column2"]
  },
  "follow_ups": ["follow-up 1", "follow-up 2"]
}

For all other questions, respond ONLY like this:
{
  "response": "Give a friendly, easy-to-read explanation or summary.",
  "follow_ups": ["follow-up question 1", "follow-up question 2"]
}

Do NOT say 'Here is your result' or 'Based on the dataset...' — just give the insight directly.
"""

    query_prompt = f"""Dataset Columns: {schema}
Sample Data: {preview}
User Query: {user_query}"""

    try:
        logger.info(f"[User Query] {user_query}")
        logger.info(f"[Columns] {schema}")
        logger.info(f"[Model Source] {model_source}")

        # Call Groq model
        output = call_groq_model(system_prompt, query_prompt)

        logger.info(f"[LLM Raw Output] {output}")

        try:
            output = output.strip()
            parsed = json.loads(output)

            if "response" not in parsed:
                raise ValueError("Missing 'response' in LLM output.")
            if "follow_ups" not in parsed:
                parsed["follow_ups"] = []

            return parsed

        except Exception as parse_error:
            logger.warning(f"[Fallback to raw text] {parse_error}")
            return {
                "response": output.replace("Here is the response:", "").replace("Based on the dataset,", "").strip(),
                "follow_ups": []
            }

    except Exception as e:
        logger.error(f"[LLM Handler Error] {e}")
        return {
            "response": f"❌ LLM Error: {e}",
            "follow_ups": []
        }
