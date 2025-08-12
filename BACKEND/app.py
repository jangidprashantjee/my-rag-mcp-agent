from flask import Flask
from routes import llm_routes
from flask_cors import CORS # only for development


app = Flask(__name__)
CORS(app, origins=["https://sampledemo-n8e7.onrender.com"])
app.register_blueprint(llm_routes)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
