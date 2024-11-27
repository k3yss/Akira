from networkx import exception
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from core.file_handling import FileHandler
from core.extraction import TopicExtractor
from core.mermaid_generator import TopicConnector, MermaidGenerator

app = Flask(__name__)
CORS(app)  # Enable CORS

UPLOAD_FOLDER = "uploads/"


@app.route("/upload", methods=["POST"])
def upload():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return jsonify({"message": "File uploaded successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("analyze/", methods=["GET"])
def analyze():
    try:
        file_handler = FileHandler()
        topic_extractor = TopicExtractor()
        topic_connector = TopicConnector()
        mermaid_gen = MermaidGenerator()

        processed_files = file_handler.process_directory(UPLOAD_FOLDER)

        if not processed_files:
            return jsonify({"error": "No files found in upload directory"})

        file_topics = {}
        for filename, content in processed_files.items():
            topics, scores = topic_extractor.extract_topics(content)
            topic_connector.add_file_topics(filename, topics, dict(scores))
            file_topics[filename] = {"topics": topics, "scores": dict(scores)}

        connections = topic_connector.find_connections()
        mermaid_diagram = mermaid_gen.create_mindmap(file_topics, connections)
        encoded_diagram = base64.b64encode(mermaid_diagram.encode("utf-8")).decode(
            "utf-8"
        )

        return jsonify({"diagram": encoded_diagram, "raw_diagram": mermaid_diagram})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.after_request
def cleanup(response):
    """Cleanup uploaded file after sucessfully processing"""
    try:
        if request.endpoint == "analyze" and response.status_code == 200:
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    except Exception as e:
        print(f"Error during cleanup: {e}")
    return response


if __name__ == "__main__":
    app.run(debug=True)
