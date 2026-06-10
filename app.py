import gradio as gr
from analyzer import analyze_job_match, optimize_resume
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

# Build Gradio UI with Tabs
with gr.Blocks(theme=gr.themes.Soft(), title="HireReady AI") as demo:

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

if __name__ == "__main__":
    demo.launch()