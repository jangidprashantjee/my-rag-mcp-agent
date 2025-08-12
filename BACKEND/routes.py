from flask import Blueprint, request, jsonify
from groq import call_llm
from websearch import webRAG_LLama3
from intent_classifier import orchestrate_query 
import os
from docsearch import load_documents_from_folder, embed_and_save_docs
from werkzeug.utils import secure_filename
from flask_cors import cross_origin

# Import necessary modules

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
    answer= orchestrate_query(prompt) #web RAG + Llama3 call
    return jsonify({"response": answer})



#######################


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@llm_routes.route('/upload-docs', methods=['POST'])
def upload_docs():
    if 'files' not in request.files:
        return jsonify({"error": "No files part in the request"}), 400

    files = request.files.getlist("files")
    saved_file_paths = []

    for file in files:
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        saved_file_paths.append(file_path)

    try:
        docs = load_documents_from_folder(saved_file_paths)
        embed_and_save_docs(docs)
        return jsonify({"message": "Documents uploaded and processed successfully."})
    except Exception as e:
        print(f"Error in /upload-docs: {e}") 
        return jsonify({"error": str(e)}), 500