from serpapi import GoogleSearch
import trafilatura
import requests
from config import SERPAPI_KEY
import json



serpapi_key = SERPAPI_KEY

def search_google(query, num_results=2):
    params = {
        "q": query,
        "api_key": serpapi_key,
        "engine": "google",
        "num": num_results
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    print(json.dumps(results, indent=2))
    return [r["link"] for r in results.get("organic_results", []) if "link" in r]

def fetch_clean_text(url):
    try:
        res = requests.get(url, timeout=10)
        downloaded = trafilatura.extract(res.text)
        return downloaded[:2000] if downloaded else ""
    except:
        return ""

def build_prompt(context, question):
    return f"""Context:
{context}

Question:
{question}

Answer:"""


def webRAG_LLama3(query):
    print(" Searching the web...")
    urls = search_google(query)
    print(f"Found {len(urls)} links. Scraping top 2.")
    context = ""
    for url in urls[:5]:
        content = fetch_clean_text(url)
        if content:
            context += content + "\n"
    if not context:
        return "No relevant info found on the web." 
    return context


#
#    prompt = build_prompt(combined_context, query)
#    print("This is from document uploaded\n"+doc_context)
#    print("\n This is from web search \n"+context)
#    return call_llm(prompt)