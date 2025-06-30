from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os
from analyzer import analyze_resume

app = Flask(__name__)
CORS(app)  # Allow access from GitHub Pages or other frontend

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        resume_file = request.files["resume"]
        jd_text = request.form["job_description"]

        # Save uploaded resume to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            resume_file.save(tmp.name)
            result = analyze_resume(tmp.name, jd_text)
            os.remove(tmp.name)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
