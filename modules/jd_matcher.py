import re


def extract_keywords(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)

    words = text.split()

    stop_words = {
        "and","or","the","is","are","of","for","to",
        "with","in","on","at","as","an","a","be","have",
        "has","will","our","your","you","we"
    }

    keywords = []

    for word in words:

        if len(word) > 2 and word not in stop_words:

            keywords.append(word)

    return list(set(keywords))


def compare_resume_with_jd(resume_text, job_description):

    resume_keywords = extract_keywords(resume_text)

    jd_keywords = extract_keywords(job_description)

    matched = []

    missing = []

    for keyword in jd_keywords:

        if keyword in resume_keywords:
            matched.append(keyword.title())

        else:
            missing.append(keyword.title())

    if len(jd_keywords) == 0:
        score = 0

    else:

        score = round((len(matched)/len(jd_keywords))*100,2)

    return score, matched, missing