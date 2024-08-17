from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
from sql import save_file_to_db, init_db

app = Flask(__name__)
CORS(app)


@app.route('/webapp.html')
def render_templ():
    return render_template('webapp.html')


@app.route('/upload_file', methods=['POST'])
def upload_file():
    upload_folder = 'uploads'
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400

    file = request.files['file']

    if file is None or file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    file_path = os.path.join(upload_folder, file.filename)
    print(file_path)

    try:
        # file.save(file_path)
        save_file_to_db(file)
        return jsonify({"status": "success", "message": "File uploaded successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "An error occurred while uploading the file"}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
