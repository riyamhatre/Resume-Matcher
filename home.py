import streamlit as st
from resume_analysis import analyze_resume
import tempfile
import os

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
