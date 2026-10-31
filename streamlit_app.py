import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="centered")
st.title("📄 AI Resume Screener")

job_desc = st.text_area("Paste Job Description Here", height=150)
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.button("🔍 Check Match", type="primary"):
    if job_desc and resume_file:
        with st.spinner("AI is checking..."):
            files = {"resume": resume_file}
            data = {"job_description": job_desc}
            response = requests.post("http://127.0.0.1:8000/match/", data=data, files=files)
            result = response.json()
            st.success(f"Match Score: {result['match_score']} - {result['status']}")
    else:
        st.warning("Please upload resume and paste job description!")