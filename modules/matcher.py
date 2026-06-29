import pandas as pd

def load_jobs():
    jobs = pd.read_csv("data/jobs.csv")
    return jobs


def calculate_match(resume_skills, job_skills):

    job_skills = [skill.strip().lower() for skill in job_skills.split(",")]
    resume_skills = [skill.lower() for skill in resume_skills]

    matched = []

    for skill in resume_skills:
        if skill in job_skills:
            matched.append(skill.title())

    score = (len(matched) / len(job_skills)) * 100

    return round(score, 2), matched


def get_missing_skills(resume_skills, job_skills):

    job_skills = [skill.strip().lower() for skill in job_skills.split(",")]
    resume_skills = [skill.lower() for skill in resume_skills]

    missing = []

    for skill in job_skills:
        if skill not in resume_skills:
            missing.append(skill.title())

    return missing