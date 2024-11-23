from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_cors import CORS

from chatbot import DocsMasterProcess, LLMRAG
from config import Config

import os
import uuid

app = Flask(__name__)
CORS(app)

processor = DocsMasterProcess()
llm_bot = LLMRAG()

if not os.path.exists(Config.PDF_FOLDER):
    os.makedirs(Config.PDF_FOLDER)

@app.before_request
def before_request():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        print("User ID created:", session['user_id'])

@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        print(f"Error rendering index: {e}")
        return jsonify({"error": "An error occurred while loading the index page."}), 500

@app.route("/add-doc", methods=["POST"])
def add_doc():
    try:
        pdf_file = request.files["pdf"]
        pdf_file.save(pdf_file.filename)

        file_path = os.path.join(Config.PDF_FOLDER, pdf_file.filename)

        processor.add(file_path)
        print("Document added to chromadb successfully!")

        return jsonify({"message": "Document added to chromadb successfully!"})
    except Exception as e:
        print(f"Error adding document: {e}")
        return jsonify({"error": "An error occurred while adding the document."}), 500

@app.route("/delete-doc", methods=["POST"])
def delete_doc():
    try:
        file_name = request.form["file_name"]
        file_path = os.path.join(Config.PDF_FOLDER, file_name)

        processor.delete(file_path)
        os.remove(file_path)

        return jsonify({"message": "Document deleted from chromadb successfully!"})
    except FileNotFoundError:
        return jsonify({"error": "File not found."}), 404
    except Exception as e:
        print(f"Error deleting document: {e}")
        return jsonify({"error": "An error occurred while deleting the document."}), 500

@app.route("/update-doc", methods=["POST"])
def update_doc():
    try:
        pdf_file = request.files["pdf"]
        pdf_file.save(pdf_file.filename)

        file_path = os.path.join(Config.PDF_FOLDER, pdf_file.filename)

        processor.update(file_path)
        print("Document updated in chromadb successfully!")

        return jsonify({"message": "Document updated in chromadb successfully!"})
    except Exception as e:
        print(f"Error updating document: {e}")
        return jsonify({"error": "An error occurred while updating the document."}), 500

@app.route("/process-prompt", methods=["POST"])
def answer():
    try:
        user_prompt = request.json.get("prompt")
        user_id = session['user_id']

        response, source_doc = llm_bot.process_prompt(user_prompt, user_id)
        print(response)
        print()
        print()
        print()
        print()
        print(source_doc)

        return jsonify({"response": response, "source_doc": source_doc})
    except Exception as e:
        print(f"Error processing prompt: {e}")
        return jsonify({"error": "An error occurred while processing the prompt."}), 500

if __name__ == "__main__":
    try:
        app.run(port=5000, debug=True)
    except Exception as e:
        print(f"Error starting the server: {e}")
