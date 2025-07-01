import streamlit as st
import pdfplumber
import docx
import re
from sentence_transformers import SentenceTransformer, util
import textstat
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
nltk.download('punkt_tab')
# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')
# Text extraction
import tempfile
import os
import sys
sys.modules['sentencepiece'] = None

st.set_page_config(page_title="Resume Matcher", layout="centered")

st.title("📝 Resume Matcher")
st.markdown("Upload your resume and paste the job description to see the match.")

uploaded_file = st.file_uploader("Upload your resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
job_description = st.text_area("Paste the job description here", height=200)

if st.button("Analyze") and uploaded_file and job_description:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    def extract_text(filepath):
        if filepath.endswith(".pdf"):
            with pdfplumber.open(filepath) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        elif filepath.endswith(".docx"):
            doc = docx.Document(filepath)
            return "\n".join(p.text for p in doc.paragraphs)
        elif filepath.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise ValueError("Unsupported file type")
    def extract_keywords(text):
        return set(re.findall(r'\b[a-zA-Z]{3,}\b', text.lower()))
    
    def remove_stopwords(text):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        return ' '.join(w for w in word_tokens if w.lower() not in stop_words and w not in string.punctuation)
    
    def analyze_resume(resume_path, jd):
        resume_text = extract_text(resume_path).replace('\n', ' ')
        jd_text = jd
        resume_text = remove_stopwords(resume_text)
        jd_text = remove_stopwords(jd_text)
        # Semantic similarity
        resume_vec = model.encode(resume_text)
        jd_vec = model.encode(jd_text)
        similarity = util.cos_sim(resume_vec, jd_vec).item()
    
        # Keyword comparison
        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(jd_text)
    
        common = resume_keywords & jd_keywords
        missing = jd_keywords - resume_keywords
        match_score = 100 * len(common) / len(jd_keywords) if jd_keywords else 0
    
    
        # Readability
        readability = textstat.flesch_reading_ease(resume_text)
    
        # Results
        return {
            "semantic_similarity": round(similarity * 100, 2),
            "keyword_match_score": round(match_score, 2),
            "common_keywords": sorted(common),
            "missing_keywords": sorted(missing),
            "readability_score": round(readability, 2)
        }

    # Analyze the resume
    with st.spinner("Analyzing your resume..."):
        result = analyze_resume(tmp_path, job_description)

    os.remove(tmp_path)

    # Show the results
    st.success("Analysis complete!")
    st.metric("Semantic Similarity", f"{result['semantic_similarity']}%")
    st.metric("Keyword Match Score", f"{result['keyword_match_score']}%")
    st.metric("Readability Score", result["readability_score"])

    st.subheader("✅ Common Keywords")
    st.write(", ".join(result["common_keywords"]))

    st.subheader("❌ Missing Keywords")
    st.write(", ".join(result["missing_keywords"]))
