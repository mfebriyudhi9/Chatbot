from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.route("/")
def index():
    pass

app.route("/add-doc", methods=["POST"])
def add_doc():
    pass

app.reoute("/process-prompt", methods=["POST"])
def answer():
    pass

if __name__ == "__main__":
    app.run()