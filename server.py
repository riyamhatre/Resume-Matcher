from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import tempfile
import os
from analyzer import analyze_resume

app = FastAPI()

# Allow frontend like GitHub Pages to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with exact origin for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisResponse(BaseModel):
    semantic_similarity: float
    keyword_match_score: float
    education_score: int
    interview_likelihood: float
    common_keywords: list[str]
    missing_keywords: list[str]
    readability_score: float

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume_endpoint(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            contents = await resume.read()
            tmp.write(contents)
            tmp_path = tmp.name

        result = analyze_resume(tmp_path, job_description)
        os.remove(tmp_path)
        return result

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
