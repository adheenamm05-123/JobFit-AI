def extract_skills(resume_text):

    skills_list = [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "machine learning",
        "deep learning",
        "pandas",
        "numpy",
        "matplotlib",
        "scikit-learn",
        "tensorflow",
        "keras",
        "opencv",
        "streamlit",
        "git",
        "github"
    ]

    resume_text = resume_text.lower()

    found_skills = []

    for skill in skills_list:
        if skill in resume_text:
            found_skills.append(skill.title())

    return found_skills