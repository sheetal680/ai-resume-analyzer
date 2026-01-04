def generate_tips(weaknesses):
    tips = []

    for w in weaknesses:
        if "internship" in w.lower():
            tips.append(
                "Add internships, freelance projects, or industry experience to improve credibility."
            )
        if "brief" in w.lower():
            tips.append(
                "Expand bullet points with measurable achievements, tools used, and outcomes."
            )
        if "extract" in w.lower():
            tips.append(
                "Ensure the resume is text-based and not a scanned image PDF."
            )

    return tips
