from flask import Flask, request, jsonify
from analyzer import analyze_resume
import tempfile
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows frontend on GitHub Pages to call backend

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        file = request.files["resume"]
        jd = request.form["job_description"]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            file.save(tmp.name)
            result = analyze_resume(tmp.name, jd)
            os.unlink(tmp.name)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
