import streamlit as st

st.set_page_config(page_title="Resume Matcher", layout="centered")

# Inject CSS styles
st.markdown("""
    <style>
        .title {
            font-size: 40px;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 30px;
        }
        .upload-section {
            border: 2px dashed #ccc;
            padding: 20px;
            border-radius: 10px;
            background-color: #f9f9f9;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# HTML content with styled class
st.markdown('<div class="title">Resume Matcher App</div>', unsafe_allow_html=True)

st.markdown('<div class="upload-section">Upload your resume below</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose your resume file", type=["pdf", "docx", "txt"])
