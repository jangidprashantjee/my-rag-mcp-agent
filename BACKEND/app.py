from flask import Flask
from routes import llm_routes
from flask_cors import CORS # only for development
import os

app = Flask(__name__)
CORS(app, origins=["https://sampledemo-n8e7.onrender.com"])
#CORS(app, origins=["*"])  # Allow all origins for development
app.register_blueprint(llm_routes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

