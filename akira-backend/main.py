from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from core.file_handling import FileHandler
from core.extraction import TopicExtractor
from core.mermaid_generator import TopicConnector, MermaidGenerator
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)
CORS(app)  # Enable CORS
UPLOAD_FOLDER = "uploads/"


@app.route("/upload", methods=["POST"])
def upload():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Get all files from the request
    files = []
    for key in request.files:
        print(key)
        if key.startswith("file"):  # This will match 'file', 'file1', 'file2', etc.
            files.append(request.files[key])

    # Check if any files were uploaded
    if not files:
        return jsonify({"error": "No files part"}), 400

    # Check if any files were selected
    if all(file.filename == "" for file in files):
        return jsonify({"error": "No selected files"}), 400

    try:
        uploaded_files = []
        for file in files:
            if file.filename:  # Check if filename is not empty
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                uploaded_files.append(file.filename)

        if uploaded_files:
            result = analyze()
            print(result)
            return jsonify(
                {
                    "message": f"Successfully uploaded {len(uploaded_files)} files",
                    "files": uploaded_files,
                    "analysis": result,
                }
            )
        else:
            return jsonify({"error": "No valid files were uploaded"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def analyze():
    file_handler = FileHandler()
    topic_extractor = TopicExtractor()
    topic_connector = TopicConnector()
    mermaid_gen = MermaidGenerator()

    # Process all files in upload directory
    processed_files = file_handler.process_directory(UPLOAD_FOLDER)
    # print(processed_files)
    if not processed_files:
        return {"error": "No files found in upload directory"}

    file_topics = {}
    for filename, content in processed_files.items():
        topics = topic_extractor.extract_topics(content)
        # print(topics)
        scores = topic_extractor.get_topic_scores(content)
        # print(scores)
        topic_connector.add_file_topics(filename, topics, dict(scores))
        # print("hallo")
        file_topics[filename] = {"topics": topics, "scores": dict(scores)}
        # print(file_topics)

    connections = topic_connector.find_connections()
    print("hallo")
    mermaid_diagram = mermaid_gen.create_mindmap(file_topics, connections)
    encoded_diagram = base64.b64encode(mermaid_diagram.encode("utf-8")).decode("utf-8")

    return {
        "diagram": encoded_diagram,
        "raw_diagram": mermaid_diagram,
        "file_topics": file_topics,
        "connections": connections,
    }


@app.after_request
def cleanup(response):
    """Cleanup uploaded files after successfully processing"""
    try:
        if request.endpoint in ["upload", "analyze"] and response.status_code == 200:
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    except Exception as e:
        print(f"Error during cleanup: {e}")
    return response


if __name__ == "__main__":
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")
    nltk.download("averaged_perceptron_tagger")
    app.run(debug=True)
