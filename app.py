import streamlit as st
from analyzer.pdf_reader import extract_text_from_pdf
from analyzer.text_cleaner import clean_text
from analyzer.ats_scorer import calculate_ats_score
from analyzer.strengths_weaknesses import analyze_strengths_weaknesses
from analyzer.tips_generator import generate_tips
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import re

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

st.title("AI Resume Analyzer with ATS Score & Smart Insights")
st.write("Upload your resume to receive ATS scoring, strengths, weaknesses, and improvement recommendations.")

# ---------------- LAYOUT ----------------
col_left, col_right = st.columns([1, 1])

with col_left:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF only)", type=["pdf"])

with col_right:
    jd_text = st.text_area(
        "📋 Paste Job Description (Optional)",
        placeholder="Paste the job description here to get a JD match score...",
        height=150
    )

if uploaded_file:
    raw_text = extract_text_from_pdf(uploaded_file)
    cleaned_text = clean_text(raw_text)

    with open("assets/keywords.txt", "r", encoding="utf-8") as f:
        keywords = [k.strip() for k in f.read().split(",") if k.strip()]

    ats_score = calculate_ats_score(cleaned_text, keywords)
    strengths, weaknesses = analyze_strengths_weaknesses(cleaned_text)
    tips = generate_tips(weaknesses)

    # ---------------- JD MATCH SCORE ----------------
    jd_score = None
    missing_jd_keywords = []

    if jd_text.strip():
        jd_words = re.findall(r'\b\w+\b', jd_text.lower())
        resume_words = set(re.findall(r'\b\w+\b', cleaned_text.lower()))
        important_jd = [w for w in jd_words if len(w) > 4]
        matched_jd_keywords = [w for w in important_jd if w in resume_words]
        missing_jd_keywords = list(set([w for w in important_jd if w not in resume_words]))[:10]
        jd_score = int((len(matched_jd_keywords) / max(len(important_jd), 1)) * 100)

    # ---------------- SCORES ----------------
    st.markdown("---")
    score_col1, score_col2 = st.columns(2)

    with score_col1:
        st.subheader("📊 ATS Compatibility Score")
        st.progress(ats_score / 100)
        color = "green" if ats_score >= 70 else "orange" if ats_score >= 50 else "red"
        st.markdown(f"<h2 style='color:{color}'>{ats_score} / 100</h2>", unsafe_allow_html=True)

    with score_col2:
        st.subheader("🎯 Job Description Match")
        if jd_score is not None:
            st.progress(jd_score / 100)
            color2 = "green" if jd_score >= 70 else "orange" if jd_score >= 50 else "red"
            st.markdown(f"<h2 style='color:{color2}'>{jd_score} / 100</h2>", unsafe_allow_html=True)
        else:
            st.info("Paste a job description above to see your JD match score.")

    # ---------------- SKILL GAP CHART ----------------
    st.markdown("---")
    st.subheader("📈 Skill Gap Analysis")

    skill_keywords = [
        "python", "machine learning", "deep learning", "nlp", "sql",
        "data analysis", "tensorflow", "pytorch", "api", "git"
    ]
    resume_lower = cleaned_text.lower()
    skill_values = [1 if s in resume_lower else 0 for s in skill_keywords]
    colors = ["#4CAF50" if v == 1 else "#F44336" for v in skill_values]

    fig, ax = plt.subplots(figsize=(10, 3))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    ax.barh(skill_keywords, skill_values, color=colors)
    ax.set_xlim(0, 1.5)
    ax.set_xticks([])
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_visible(False)
    for i, val in enumerate(skill_values):
        ax.text(val + 0.05, i, "✓ Present" if val == 1 else "✗ Missing",
                va='center', color='white', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)

    # ---------------- STRENGTHS & WEAKNESSES ----------------
    st.markdown("---")
    sw_col1, sw_col2 = st.columns(2)

    with sw_col1:
        st.subheader("💪 Strengths")
        if strengths:
            for s in strengths:
                st.success(s)
        else:
            st.info("No major strengths detected.")

    with sw_col2:
        st.subheader("⚠️ Weaknesses")
        if weaknesses:
            for w in weaknesses:
                st.warning(w)
        else:
            st.success("No critical weaknesses detected.")

    # ---------------- TOP 5 IMPROVEMENTS ----------------
    st.markdown("---")
    st.subheader("🛠 Top 5 Improvement Recommendations")
    top_tips = tips[:5] if tips else ["Your resume is well optimized!"]
    for i, t in enumerate(top_tips, 1):
        st.info(f"**{i}.** {t}")

    # ---------------- MISSING JD KEYWORDS ----------------
    if missing_jd_keywords:
        st.markdown("---")
        st.subheader("🔍 Keywords Missing from Job Description")
        st.markdown("Add these keywords to your resume to improve your JD match score:")
        cols = st.columns(5)
        for i, kw in enumerate(missing_jd_keywords):
            cols[i % 5].error(f"`{kw}`")

    # ---------------- PDF DOWNLOAD ----------------
    st.markdown("---")
    st.subheader("📥 Download Your Report")

    def generate_pdf_report():
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "AI Resume Analysis Report", ln=True, align="C")
            pdf.ln(5)

            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 10, f"ATS Score: {ats_score} / 100", ln=True)
            if jd_score is not None:
                pdf.cell(0, 10, f"JD Match Score: {jd_score} / 100", ln=True)
            pdf.ln(3)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Strengths:", ln=True)
            pdf.set_font("Arial", size=11)
            for s in strengths:
                pdf.multi_cell(0, 8, f"  + {s}")

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Weaknesses:", ln=True)
            pdf.set_font("Arial", size=11)
            for w in weaknesses:
                pdf.multi_cell(0, 8, f"  - {w}")

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Top Improvements:", ln=True)
            pdf.set_font("Arial", size=11)
            for i, t in enumerate(top_tips, 1):
                pdf.multi_cell(0, 8, f"  {i}. {t}")

            if missing_jd_keywords:
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, "Missing JD Keywords:", ln=True)
                pdf.set_font("Arial", size=11)
                pdf.multi_cell(0, 8, ", ".join(missing_jd_keywords))

            return pdf.output(dest='S').encode('latin-1')
        except ImportError:
            return None

    pdf_bytes = generate_pdf_report()
    if pdf_bytes:
        st.download_button(
            label="⬇️ Download PDF Report",
            data=pdf_bytes,
            file_name="resume_analysis_report.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("To enable PDF download, add `fpdf2` to your requirements.txt")