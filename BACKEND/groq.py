from openai import OpenAI
from config import GROQ_API_KEY, GROQ_API_BASE, GROQ_MODEL

client = OpenAI(
    base_url=GROQ_API_BASE,
    api_key=GROQ_API_KEY
)

def call_llm(query):
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL, # we can change model in config 
            messages=[
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during LLM call: {e}"
