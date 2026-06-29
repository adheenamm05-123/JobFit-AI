def calculate_ats_score(resume_text, job_description):

    resume_words = set(resume_text.lower().split())
    jd_words = set(job_description.lower().split())

    if len(jd_words) == 0:
        return 0

    matched = resume_words.intersection(jd_words)

    score = (len(matched) / len(jd_words)) * 100

    if score > 100:
        score = 100

    return round(score, 2)


def resume_strength(score):

    if score >= 85:
        return "Excellent ⭐⭐⭐⭐⭐"

    elif score >= 70:
        return "Good ⭐⭐⭐⭐"

    elif score >= 50:
        return "Average ⭐⭐⭐"

    else:
        return "Needs Improvement ⭐⭐"