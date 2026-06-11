import gradio as gr
from analyzer import analyze_job_match, optimize_resume, generate_interview_questions, evaluate_answer, get_market_intelligence, generate_learning_roadmap
import PyPDF2
import io

# Extract text from PDF
def extract_pdf_text(pdf_file):
    if pdf_file is None:
        return ""
    with open(pdf_file, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Job Match Analysis
def analyze(resume_pdf, resume_text, job_description):
    if resume_pdf is not None:
        final_resume = extract_pdf_text(resume_pdf)
    elif resume_text.strip():
        final_resume = resume_text
    else:
        return "❌ Please provide your resume!", "", "", "", ""

    if not job_description.strip():
        return "❌ Please provide the job description!", "", "", "", ""

    result = analyze_job_match(final_resume, job_description)

    lines = result.split('\n')
    score = 0
    verdict = ""
    skills_have = []
    skills_missing = []
    strengths = []
    recommendation = ""
    parsing = ""

    for line in lines:
        if line.startswith("MATCH_SCORE:"):
            try:
                score = int(line.split(":")[1].strip())
            except:
                score = 0
        elif "SKILLS_YOU_HAVE:" in line:
            parsing = "have"
        elif "SKILLS_YOU_MISSING:" in line:
            parsing = "missing"
        elif "STRENGTHS:" in line:
            parsing = "strengths"
        elif "RECOMMENDATION:" in line:
            parsing = "recommendation"
        elif "VERDICT:" in line:
            verdict = line.split(":")[1].strip()
            parsing = ""
        elif line.startswith("- ") and parsing == "have":
            skills_have.append(f"✅ {line[2:]}")
        elif line.startswith("- ") and parsing == "missing":
            skills_missing.append(f"❌ {line[2:]}")
        elif line.startswith("- ") and parsing == "strengths":
            strengths.append(f"💪 {line[2:]}")
        elif parsing == "recommendation" and line.strip():
            recommendation += line + " "

    score_display = f"## 🎯 Match Score: {score}%\n### Verdict: {verdict}"
    skills_have_display = "\n".join(skills_have)
    skills_missing_display = "\n".join(skills_missing)
    strengths_display = "\n".join(strengths)

    return score_display, skills_have_display, skills_missing_display, strengths_display, recommendation

# Resume Optimizer
def optimize(resume_pdf, resume_text, job_description):
    if resume_pdf is not None:
        final_resume = extract_pdf_text(resume_pdf)
    elif resume_text.strip():
        final_resume = resume_text
    else:
        return "❌ Please provide your resume!", "", "", ""

    if not job_description.strip():
        return "❌ Please provide the job description!", "", "", ""

    result = optimize_resume(final_resume, job_description)

    lines = result.split('\n')
    score_before = 0
    score_after = 0
    keywords = []
    changes = []
    optimized_resume = ""
    parsing = ""

    for line in lines:
        if line.startswith("ATS_SCORE_BEFORE:"):
            try:
                score_before = int(line.split(":")[1].strip())
            except:
                score_before = 0
        elif line.startswith("ATS_SCORE_AFTER:"):
            try:
                score_after = int(line.split(":")[1].strip())
            except:
                score_after = 0
        elif "KEYWORDS_ADDED:" in line:
            parsing = "keywords"
        elif "OPTIMIZED_RESUME:" in line:
            parsing = "resume"
        elif "CHANGES_MADE:" in line:
            parsing = "changes"
        elif line.startswith("- ") and parsing == "keywords":
            keywords.append(f"🔑 {line[2:]}")
        elif line.startswith("- ") and parsing == "changes":
            changes.append(f"✏️ {line[2:]}")
        elif parsing == "resume" and line.strip():
            optimized_resume += line + "\n"

    scores_display = f"## 📈 ATS Score Improvement\n### Before: {score_before}% → After: {score_after}%"
    keywords_display = "\n".join(keywords)
    changes_display = "\n".join(changes)

    return scores_display, keywords_display, optimized_resume, changes_display

# Generate Questions
def generate_questions(job_description):
    if not job_description.strip():
        return "❌ Please provide the job description!", "", "", "", ""
    
    result = generate_interview_questions(job_description)
    
    questions = []
    for line in result.split('\n'):
        if line.startswith("Q") and ":" in line:
            question = line.split(":", 1)[1].strip()
            questions.append(question)
    
    q1 = questions[0] if len(questions) > 0 else ""
    q2 = questions[1] if len(questions) > 1 else ""
    q3 = questions[2] if len(questions) > 2 else ""
    q4 = questions[3] if len(questions) > 3 else ""
    q5 = questions[4] if len(questions) > 4 else ""
    
    return q1, q2, q3, q4, q5

# Evaluate Answer
def evaluate(question, user_answer, job_description):
    if not question.strip():
        return "❌ Please generate questions first!"
    if not user_answer.strip():
        return "❌ Please write your answer!"
    
    result = evaluate_answer(question, user_answer, job_description)
    
    lines = result.split('\n')
    score = 0
    verdict = ""
    good_points = []
    missing_points = []
    perfect_answer = ""
    parsing = ""
    
    for line in lines:
        if line.startswith("SCORE:"):
            try:
                score = int(line.split(":")[1].strip())
            except:
                score = 0
        elif "WHAT_WAS_GOOD:" in line:
            parsing = "good"
        elif "WHAT_WAS_MISSING:" in line:
            parsing = "missing"
        elif "PERFECT_ANSWER:" in line:
            parsing = "perfect"
        elif "VERDICT:" in line:
            verdict = line.split(":")[1].strip()
            parsing = ""
        elif line.startswith("- ") and parsing == "good":
            good_points.append(f"✅ {line[2:]}")
        elif line.startswith("- ") and parsing == "missing":
            missing_points.append(f"❌ {line[2:]}")
        elif parsing == "perfect" and line.strip():
            perfect_answer += line + "\n"
    
    # Score emoji
    if score >= 8:
        score_emoji = "🔥"
    elif score >= 6:
        score_emoji = "👍"
    elif score >= 4:
        score_emoji = "⚠️"
    else:
        score_emoji = "❌"
    
    result_display = f"""## {score_emoji} Score: {score}/10 — {verdict}

### ✅ What Was Good:
{chr(10).join(good_points)}

### ❌ What Was Missing:
{chr(10).join(missing_points)}

### 💡 Perfect Answer:
{perfect_answer}
"""
    return result_display

def market_intelligence(job_title):
    if not job_title.strip():
        return "❌ Please enter a job title!", "", "", ""
    
    result = get_market_intelligence(job_title)
    
    lines = result.split('\n')
    skills = []
    companies = []
    salary = ""
    tips = []
    parsing = ""
    
    for line in lines:
        if "TOP_SKILLS:" in line:
            parsing = "skills"
        elif "SALARY_RANGE:" in line:
            parsing = "salary"
        elif "TOP_COMPANIES:" in line:
            parsing = "companies"
        elif "INTERVIEW_TIPS:" in line:
            parsing = "tips"
        elif line.startswith("- ") and parsing == "skills":
            skills.append(f"🔥 {line[2:]}")
        elif line.startswith("- ") and parsing == "companies":
            companies.append(f"🏢 {line[2:]}")
        elif line.startswith("- ") and parsing == "tips":
            tips.append(f"💡 {line[2:]}")
        elif parsing == "salary" and line.strip():
            salary += line + " "
    
    skills_display = "\n".join(skills)
    companies_display = "\n".join(companies)
    tips_display = "\n".join(tips)
    
    return skills_display, salary, companies_display, tips_display

def learning_roadmap(job_title):
    if not job_title.strip():
        return "❌ Please enter a job title!", "", "", ""
    
    result = generate_learning_roadmap(job_title)
    
    lines = result.split('\n')
    timeline = ""
    skills_to_learn = []
    weeks = {"WEEK1": [], "WEEK2": [], "WEEK3": [], "WEEK4": []}
    resources = []
    projects = []
    parsing = ""
    
    for line in lines:
        if line.startswith("TIMELINE:"):
            timeline = line.split(":")[1].strip()
        elif "SKILLS_TO_LEARN:" in line:
            parsing = "skills"
        elif "WEEK1:" in line:
            parsing = "WEEK1"
        elif "WEEK2:" in line:
            parsing = "WEEK2"
        elif "WEEK3:" in line:
            parsing = "WEEK3"
        elif "WEEK4:" in line:
            parsing = "WEEK4"
        elif "RESOURCES:" in line:
            parsing = "resources"
        elif "PROJECTS:" in line:
            parsing = "projects"
        elif line.startswith("- ") and parsing == "skills":
            skills_to_learn.append(f"🎯 {line[2:]}")
        elif line.startswith("- ") and parsing in weeks:
            weeks[parsing].append(f"📌 {line[2:]}")
        elif line.startswith("- ") and parsing == "resources":
            resources.append(f"📚 {line[2:]}")
        elif line.startswith("- ") and parsing == "projects":
            projects.append(f"🛠️ {line[2:]}")

    weeks_display = f"""## 🗓️ Your {timeline} Roadmap

### 🎯 Skills You Need to Learn:
{chr(10).join(skills_to_learn)}

---

### Week 1
{chr(10).join(weeks['WEEK1'])}

### Week 2
{chr(10).join(weeks['WEEK2'])}

### Week 3
{chr(10).join(weeks['WEEK3'])}

### Week 4
{chr(10).join(weeks['WEEK4'])}
"""
    resources_display = "\n".join(resources)
    projects_display = "\n".join(projects)
    
    return weeks_display, resources_display, projects_display

# Build Gradio UI with Tabs
with gr.Blocks(title="HireReady AI") as demo:

    gr.Markdown("""
    # 🎯 HireReady AI
    ### Your AI-powered career coach
    """)

    with gr.Tabs():

        # Tab 1 — Job Match Analyzer
        with gr.Tab("🎯 Job Match Analyzer"):
            gr.Markdown("### Know exactly how ready you are for any job")

            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📄 Your Resume")
                    resume_pdf_1 = gr.File(label="Upload Resume (PDF)", file_types=[".pdf"])
                    gr.Markdown("**OR paste below:**")
                    resume_text_1 = gr.Textbox(
                        label="Resume Text",
                        placeholder="Paste your resume here...",
                        lines=10
                    )
                with gr.Column():
                    gr.Markdown("### 💼 Job Description")
                    job_desc_1 = gr.Textbox(
                        label="Job Description",
                        placeholder="Paste the job description here...",
                        lines=15
                    )

            analyze_btn = gr.Button("🔍 Analyze My Match", variant="primary", size="lg")
            gr.Markdown("---")
            gr.Markdown("## 📊 Match Report")
            score_output = gr.Markdown()

            with gr.Row():
                with gr.Column():
                    skills_have_output = gr.Markdown(label="✅ Skills You Have")
                    strengths_output = gr.Markdown(label="💪 Strengths")
                with gr.Column():
                    skills_missing_output = gr.Markdown(label="❌ Skills Missing")
                    recommendation_output = gr.Markdown(label="💡 Recommendation")

            analyze_btn.click(
                fn=analyze,
                inputs=[resume_pdf_1, resume_text_1, job_desc_1],
                outputs=[score_output, skills_have_output, skills_missing_output,
                         strengths_output, recommendation_output]
            )

        # Tab 2 — Resume Optimizer
        with gr.Tab("📝 Resume Optimizer"):
            gr.Markdown("### AI rewrites your resume to match the job perfectly")

            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📄 Your Resume")
                    resume_pdf_2 = gr.File(label="Upload Resume (PDF)", file_types=[".pdf"])
                    gr.Markdown("**OR paste below:**")
                    resume_text_2 = gr.Textbox(
                        label="Resume Text",
                        placeholder="Paste your resume here...",
                        lines=10
                    )
                with gr.Column():
                    gr.Markdown("### 💼 Job Description")
                    job_desc_2 = gr.Textbox(
                        label="Job Description",
                        placeholder="Paste the job description here...",
                        lines=15
                    )

            optimize_btn = gr.Button("✨ Optimize My Resume", variant="primary", size="lg")
            gr.Markdown("---")
            gr.Markdown("## 📊 Optimization Report")
            scores_output = gr.Markdown()

            with gr.Row():
                with gr.Column():
                    keywords_output = gr.Markdown(label="🔑 Keywords Added")
                    changes_output = gr.Markdown(label="✏️ Changes Made")
                with gr.Column():
                    optimized_resume_output = gr.Textbox(
                        label="📄 Your Optimized Resume",
                        lines=20
                    )

            optimize_btn.click(
                fn=optimize,
                inputs=[resume_pdf_2, resume_text_2, job_desc_2],
                outputs=[scores_output, keywords_output, optimized_resume_output, changes_output]
            )
        # Tab 3 — AI Mock Interviewer
        with gr.Tab("🎤 AI Mock Interviewer"):
            gr.Markdown("### Practice interviews with AI feedback")

            job_desc_3 = gr.Textbox(
                label="💼 Job Description",
                placeholder="Paste the job description here...",
                lines=5
            )

            generate_btn = gr.Button("🎯 Generate Interview Questions", 
                                      variant="primary", size="lg")

            gr.Markdown("---")
            gr.Markdown("## 📝 Your Interview Questions")

            with gr.Row():
                with gr.Column():
                    q1 = gr.Textbox(label="Question 1", interactive=False)
                    q2 = gr.Textbox(label="Question 2", interactive=False)
                    q3 = gr.Textbox(label="Question 3", interactive=False)
                with gr.Column():
                    q4 = gr.Textbox(label="Question 4", interactive=False)
                    q5 = gr.Textbox(label="Question 5", interactive=False)

            generate_btn.click(
                fn=generate_questions,
                inputs=[job_desc_3],
                outputs=[q1, q2, q3, q4, q5]
            )

            gr.Markdown("---")
            gr.Markdown("## 🎤 Practice Your Answer")

            with gr.Row():
                with gr.Column():
                    selected_question = gr.Textbox(
                        label="Question to Answer",
                        placeholder="Copy any question from above and paste here...",
                        lines=3
                    )
                    user_answer = gr.Textbox(
                        label="Your Answer",
                        placeholder="Type your answer here...",
                        lines=8
                    )
                with gr.Column():
                    feedback_output = gr.Markdown(label="AI Feedback")

            evaluate_btn = gr.Button("🔍 Evaluate My Answer", 
                                      variant="primary", size="lg")

            evaluate_btn.click(
                fn=evaluate,
                inputs=[selected_question, user_answer, job_desc_3],
                outputs=[feedback_output]
            )

        # Tab 4 — Market Intelligence
        with gr.Tab("🔍 Market Intelligence"):
            gr.Markdown("### Real-time job market insights for any role")

            with gr.Row():
                job_title_input = gr.Textbox(
                    label="💼 Job Title",
                    placeholder="e.g. AI Engineer, Data Scientist, ML Engineer...",
                    scale=4
                )
                search_btn = gr.Button("🔍 Search Market", variant="primary", scale=1)

            gr.Markdown("---")
            gr.Markdown("## 📊 Market Report")

            with gr.Row():
                with gr.Column():
                    skills_market_output = gr.Markdown(label="🔥 Top Skills Required")
                    salary_output = gr.Markdown(label="💰 Salary Range")
                with gr.Column():
                    companies_output = gr.Markdown(label="🏢 Top Companies Hiring")
                    tips_output = gr.Markdown(label="💡 Interview Tips")

            search_btn.click(
                fn=market_intelligence,
                inputs=[job_title_input],
                outputs=[skills_market_output, salary_output, 
                         companies_output, tips_output]
            )
        
        # Tab 5 — Learning Roadmap
        with gr.Tab("🗺️ Learning Roadmap"):
            gr.Markdown("### Get a personalized plan to become job ready")

            roadmap_job_title = gr.Textbox(
                label="🎯 What job do you want?",
                placeholder="e.g. AI Engineer, Data Scientist, ML Engineer..."
            )

            roadmap_btn = gr.Button("🗺️ Generate My Roadmap",
                                     variant="primary", size="lg")
            gr.Markdown("---")

            weeks_output = gr.Markdown()

            with gr.Row():
                with gr.Column():
                    resources_output = gr.Markdown(label="📚 Resources")
                with gr.Column():
                    projects_output = gr.Markdown(label="🛠️ Projects to Build")

            roadmap_btn.click(
                fn=learning_roadmap,
                inputs=[roadmap_job_title],
                outputs=[weeks_output, resources_output, projects_output]
            )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())