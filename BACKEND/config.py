import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_BASE = "https://api.groq.com/openai/v1"
GROQ_MODEL = "llama3-8b-8192" # text to text  , code  , no audio  , video or image , no web searches
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DB_PATH = "vectorstore/db_faiss"
