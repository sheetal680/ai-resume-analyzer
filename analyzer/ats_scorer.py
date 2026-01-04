def calculate_ats_score(text, keywords):
    if not text or not keywords:
        return 0

    keyword_matches = sum(1 for kw in keywords if kw.lower() in text)
    keyword_score = (keyword_matches / len(keywords)) * 70

    word_count = len(text.split())
    length_score = 30 if word_count >= 300 else (word_count / 300) * 30

    final_score = int(keyword_score + length_score)
    return min(final_score, 100)
