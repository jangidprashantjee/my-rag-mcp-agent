from flask import Blueprint, request, jsonify
from groq import call_llm
from websearch import webRAG_LLama3
from intent_classifier import orchestrate_query 
import os
from docsearch import load_documents_from_folder, embed_and_save_docs
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
from flask import Response, stream_with_context, request, jsonify
import time
# Import necessary modules

llm_routes = Blueprint('llm_routes', __name__)


@llm_routes.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Query is required"}), 400

    def generate():
        for chunk in orchestrate_query(prompt):
            yield chunk
            time.sleep(0.01)  

    return Response(stream_with_context(generate()), mimetype="text/plain")
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