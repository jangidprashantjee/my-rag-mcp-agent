from flask import Blueprint, request, jsonify
from groq import call_llm
from websearch import webRAG_LLama3

llm_routes = Blueprint('llm_routes', __name__)

@llm_routes.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt")
    print("Headers:", request.headers)
    print("Data raw:", request.data)
    print("JSON:", request.get_json(force=True))
    if not prompt:
        return jsonify({"error": "Query is required"}), 400

    #answer = call_llm(prompt) # Dummy call data
    answer= webRAG_LLama3(prompt) #web RAG + Llama3 call
    return jsonify({"response": answer})
