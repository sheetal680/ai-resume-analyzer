def analyze_strengths_weaknesses(text):
    strengths = []
    weaknesses = []

    if not text:
        weaknesses.append("Resume text could not be extracted properly")
        return strengths, weaknesses

    technical_skills = ["python", "java", "sql", "machine learning", "data analysis"]
    if any(skill in text for skill in technical_skills):
        strengths.append("Strong technical skill presence")

    if "project" in text:
        strengths.append("Hands-on project experience")

    if "internship" not in text:
        weaknesses.append("Internship or real-world experience not mentioned")

    if len(text.split()) < 300:
        weaknesses.append("Resume content is too brief for ATS optimization")

    return strengths, weaknesses
