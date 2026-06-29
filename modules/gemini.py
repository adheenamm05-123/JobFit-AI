import google.generativeai as genai

API_KEY = "YOUR_API_KEY"
genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")


def get_ai_suggestions(resume_text):

    prompt = f"""
    You are a professional career advisor.

    Analyze this resume.

    Resume:

    {resume_text}

    Give:

    1. Strengths
    2. Weaknesses
    3. Missing Skills
    4. Career Suggestions

    Keep the answer short.
    """

    response = model.generate_content(prompt)

    return response.text