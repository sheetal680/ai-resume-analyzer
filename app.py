import streamlit as st
from analyzer.pdf_reader import extract_text_from_pdf
from analyzer.text_cleaner import clean_text
from analyzer.ats_scorer import calculate_ats_score
from analyzer.strengths_weaknesses import analyze_strengths_weaknesses
from analyzer.tips_generator import generate_tips

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="centered"
)

st.title("AI Resume Analyzer with ATS Score & Smart Insights")
st.write(
    "Upload your resume to receive ATS scoring, strengths, weaknesses, and improvement recommendations."
)

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded_file:
    raw_text = extract_text_from_pdf(uploaded_file)
    cleaned_text = clean_text(raw_text)

    with open("assets/keywords.txt", "r", encoding="utf-8") as f:
        keywords = [k.strip() for k in f.read().split(",") if k.strip()]

    ats_score = calculate_ats_score(cleaned_text, keywords)
    strengths, weaknesses = analyze_strengths_weaknesses(cleaned_text)
    tips = generate_tips(weaknesses)

    st.subheader("📊 ATS Compatibility Score")
    st.progress(ats_score / 100)
    st.write(f"**{ats_score} / 100**")

    st.subheader("💪 Strengths")
    if strengths:
        for s in strengths:
            st.success(s)
    else:
        st.info("No major strengths detected based on ATS signals.")

    st.subheader("⚠️ Weaknesses")
    if weaknesses:
        for w in weaknesses:
            st.warning(w)
    else:
        st.success("No critical weaknesses detected.")

    st.subheader("🛠 Improvement Recommendations")
    if tips:
        for t in tips:
            st.info(t)
    else:
        st.success("Your resume is well optimized for ATS systems.")
