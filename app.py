from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from resume_analysis import analyze_resume

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile, jd: str = Form(...)):
    contents = await file.read()
    with open(file.filename, "wb") as f:
        f.write(contents)
    results = analyze_resume(file.filename, jd)
    return JSONResponse(content=results)
