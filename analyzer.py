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

from duckduckgo_search import DDGS

def get_market_intelligence(job_title):
    with DDGS() as ddgs:
        skills_search = list(ddgs.text(
            f"{job_title} required skills technologies 2026", max_results=5))
        
        salary_search = list(ddgs.text(
            f"{job_title} salary India freshers 2026 lakhs per annum", max_results=5))
        
        companies_search = list(ddgs.text(
            f"top companies hiring {job_title} India Bangalore Chennai Hyderabad", max_results=5))
        
        interview_search = list(ddgs.text(
            f"{job_title} interview questions topics asked 2026", max_results=5))

    all_results = f"""
SKILLS SEARCH:
{' '.join([r['body'] for r in skills_search])}

SALARY SEARCH:
{' '.join([r['body'] for r in salary_search])}

COMPANIES SEARCH:
{' '.join([r['body'] for r in companies_search])}

INTERVIEW SEARCH:
{' '.join([r['body'] for r in interview_search])}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a job market analyst in India.
Extract and summarize real information from these search results.
Be specific with numbers, company names, and skills.
If data is available use it, don't say "not provided".

Respond in this EXACT format:

TOP_SKILLS:
- [skill 1]
- [skill 2]
- [skill 3]
- [skill 4]
- [skill 5]

SALARY_RANGE:
[specific salary range in LPA for India freshers]

TOP_COMPANIES:
- [company 1]
- [company 2]
- [company 3]
- [company 4]
- [company 5]

INTERVIEW_TIPS:
- [specific topic 1]
- [specific topic 2]
- [specific topic 3]
- [specific topic 4]
- [specific topic 5]"""
            },
            {
                "role": "user",
                "content": f"Job Title: {job_title} in India\n\nSearch Results:\n{all_results}"
            }
        ]
    )
    return response.choices[0].message.content

def generate_learning_roadmap(job_title):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert career coach and learning advisor.
Given a job title, figure out the most important skills to learn and create a roadmap.

Respond in this EXACT format:

SKILLS_TO_LEARN:
- [skill 1]
- [skill 2]
- [skill 3]

TIMELINE: [X weeks]

WEEK1:
- [task 1]
- [task 2]
- [task 3]

WEEK2:
- [task 1]
- [task 2]
- [task 3]

WEEK3:
- [task 1]
- [task 2]
- [task 3]

WEEK4:
- [task 1]
- [task 2]
- [task 3]

RESOURCES:
- [resource 1]
- [resource 2]
- [resource 3]

PROJECTS:
- [project 1]
- [project 2]"""
            },
            {
                "role": "user",
                "content": f"Create a complete learning roadmap for someone who wants to become: {job_title}"
            }
        ]
    )
    return response.choices[0].message.content