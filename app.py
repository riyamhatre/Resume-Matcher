from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from resume_utils import analyze_resume
import tempfile
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Resume Analyzer is up and running 🚀"}

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...), job_description: str = Form(...)):
    try:
        # Save uploaded file temporarily
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        result = analyze_resume(tmp_path, job_description)
        os.remove(tmp_path)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
