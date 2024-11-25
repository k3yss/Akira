import os
from flask import Flask, request, jsonify

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads/'


@app.route('/upload', methods=['POST'])
def upload() -> str:
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file = request.files['file']
    file.save('uploads/' + file.filename)
    return jsonify({'message': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)