import json
from groq import call_llm  
from client import call_tool
from websearch import webRAG_LLama3
from docsearch import retrieve_docs
from config import SYSTEM_PROMPT
from datetime import datetime

def classify_query(query: str):
    prompt = f"{SYSTEM_PROMPT}\n\nUser query: {query}\nIntents:"
    print("Classifying query intent with LLM...")
    response = call_llm(prompt)  
    try:
        intents = json.loads(response)
        if not isinstance(intents, list):
            raise ValueError("Invalid format")
        return intents
    except Exception:
        return []

def extract_location(query: str) -> str:
    prompt = f"""
    You are an information extraction system.
    Your task: From the query below, extract ONLY the location keyword.

    Rules:
    - Output only the location as plain text (e.g., Delhi)
    - If there is no location, output nothing at all (completely empty output)
    - Do NOT include labels, quotes, punctuation, or extra words
    - Do NOT explain your answer

    Query: {query}
    """
    location = call_llm(prompt).strip()
    return location






def extract_date(query: str) -> str:
    prompt = f"""
    Extract the date mentioned in this query. If the query contains relative dates like "today", "tomorrow", or "yesterday", 
    convert them to the actual date in YYYY-MM-DD format assuming today's date is {datetime.now().strftime('%Y-%m-%d')}. 
    If an explicit date is present (e.g., DD/MM/YYYY, YYYY-MM-DD), return it in YYYY-MM-DD format. 
    If no date is found, return an empty string.
    Only return the date string or empty string, no extra explanation.

    Query: "{query}"
    Date:
    """
    date = call_llm(prompt).strip()
    return date

def orchestrate_query(query: str):
    intents = classify_query(query)  
    print(intents)
    context_parts = []

    if "weather" in intents:
        loc = extract_location(query)
        date = extract_date(query)
        if loc:
            weather_data = call_tool("get_weather_by_location_name", {"location": loc ,"date": date})
            context_parts.append(f"Weather info:\n{weather_data}")
        else:
            context_parts.append("Weather info: No location detected in the query.")

    if "local_rag" in intents:
        rag_data = retrieve_docs(query)
        context_parts.append(f"Local document info:\n{rag_data}")

    if "web_search" in intents:
        web_data = webRAG_LLama3(query)
        context_parts.append(f"Web search results:\n{web_data}")

    enhanced_prompt = f"""
    User query: {query}

    Additional context from tools:
    {chr(10).join(context_parts)}

    Please provide a complete, well-structured answer.
    """
    print("Calling LLM with enhanced prompt...")
    print(enhanced_prompt)
    return call_llm(enhanced_prompt)
