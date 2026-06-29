def generate_suggestions(missing_skills):

    suggestions = []

    for skill in missing_skills:

        suggestions.append(f"Learn {skill}")

    suggestions.append("Build one real-world project")

    suggestions.append("Upload projects to GitHub")

    suggestions.append("Improve your resume")

    return suggestions