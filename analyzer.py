from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_job_match(resume_text, job_description):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert HR analyst and career coach. 
Analyze the resume against the job description and respond in this EXACT format:

MATCH_SCORE: [number between 0-100]

SKILLS_YOU_HAVE:
- [skill 1]
- [skill 2]
- [skill 3]

SKILLS_YOU_MISSING:
- [skill 1]
- [skill 2]
- [skill 3]

STRENGTHS:
- [strength 1]
- [strength 2]

RECOMMENDATION:
[2-3 sentences of honest advice]

VERDICT: [STRONG MATCH / GOOD MATCH / PARTIAL MATCH / NOT A MATCH]"""
            },
            {
                "role": "user",
                "content": f"""
RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Analyze and give me the match report.
"""
            }
        ]
    )
    return response.choices[0].message.content
def optimize_resume(resume_text, job_description):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert resume writer and ATS optimization specialist.
Your job is to rewrite the candidate's resume to better match the job description.

Respond in this EXACT format:

ATS_SCORE_BEFORE: [number 0-100]
ATS_SCORE_AFTER: [number 0-100]

KEYWORDS_ADDED:
- [keyword 1]
- [keyword 2]
- [keyword 3]

OPTIMIZED_RESUME:
[Full rewritten resume here]

CHANGES_MADE:
- [change 1]
- [change 2]
- [change 3]"""
            },
            {
                "role": "user",
                "content": f"""
ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Rewrite the resume to better match this job. Keep all real experience but reframe and add relevant keywords.
"""
            }
        ]
    )
    return response.choices[0].message.content
def generate_interview_questions(job_description):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert technical interviewer.
Generate 5 real interview questions for this job.
Mix of technical and behavioral questions.

Respond in this EXACT format:

Q1: [question]
Q2: [question]
Q3: [question]
Q4: [question]
Q5: [question]"""
            },
            {
                "role": "user",
                "content": f"Generate interview questions for this job:\n{job_description}"
            }
        ]
    )
    return response.choices[0].message.content


def evaluate_answer(question, user_answer, job_description):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert interviewer evaluating a candidate's answer.
Be honest, constructive and helpful.

Respond in this EXACT format:

SCORE: [number 0-10]

WHAT_WAS_GOOD:
- [point 1]
- [point 2]

WHAT_WAS_MISSING:
- [point 1]
- [point 2]

PERFECT_ANSWER:
[Write the ideal answer for this question]

VERDICT: [EXCELLENT / GOOD / NEEDS IMPROVEMENT / POOR]"""
            },
            {
                "role": "user",
                "content": f"""
JOB DESCRIPTION:
{job_description}

INTERVIEW QUESTION:
{question}

CANDIDATE'S ANSWER:
{user_answer}

Evaluate this answer.
"""
            }
        ]
    )
    return response.choices[0].message.content