"""Seeds the database with your original portfolio content the first time
the app runs against an empty database. After that, manage everything
through /admin — this file won't run again unless the DB is wiped.
You can also run it manually: `python3 seed_data.py`
"""
from models import (
    db, Profile, SkillGroup, Project, Experience, Education, Certification, Resource,
)


def run_seed():
    profile = Profile(
        id=1,
        name="Arshdeep Singh",
        roles="AI/ML Engineer (0.5 YEAR),Generative AI Developer (0 YEAR),Python Developer (01 YEAR)",
        location="Mohali, Punjab, India",
        email="arshdeepsingh17092@gmail.com",
        contact_number="+91 6284519020",
        github="https://github.com/Arshdeep6840",
        linkedin="https://www.linkedin.com/in/arshdeep-singh-ai",
        resume_file="Arshdeep_Singh_Resume.pdf",
        summary=(
            "AI/ML and Generative AI-focused Python developer who builds machine "
            "learning models, NLP workflows, LLM-powered applications and REST "
            "APIs end to end. Comfortable across the full stack of an AI "
            "product — data preprocessing and feature engineering, model "
            "training and serving, prompt engineering and RAG concepts, and "
            "shipping it behind a clean Django/Flask backend with a dashboard "
            "on top."
        ),
        stat1_label="AI/ML Projects Shipped", stat1_value="4+",
        stat2_label="Internships Completed", stat2_value="2",
        stat3_label="Core Skill Domains", stat3_value="8",
        stat4_label="Frameworks & Tools", stat4_value="20+",
    )
    db.session.add(profile)

    skill_groups = [
        dict(category="Programming",
             import_line="from languages import Python, SQL, JavaScript, HTML5, CSS3",
             tags="Python,SQL,JavaScript,HTML5,CSS3", sort_order=1),
        dict(category="AI / ML",
             import_line="from ml import Classification, Regression, FeatureEngineering",
             tags="Supervised Learning,Classification,Regression,Model Evaluation,Feature Engineering,Data Preprocessing",
             sort_order=2),
        dict(category="Deep Learning",
             import_line="from deep_learning import TensorFlow, Keras, CNN, LSTM",
             tags="TensorFlow,Keras,Neural Networks,LSTM,CNN Basics", sort_order=3),
        dict(category="Generative AI",
             import_line="from genai import LLMs, PromptEngineering, RAG",
             tags="LLMs,Prompt Engineering,Hugging Face Transformers,Sentence Transformers,RAG Concepts,AI API Integration",
             sort_order=4),
        dict(category="NLP",
             import_line="from nlp import NER, Embeddings, TextClassification",
             tags="NLTK,spaCy,Text Classification,Named Entity Recognition,Embeddings,Semantic Similarity",
             sort_order=5),
        dict(category="Data Science",
             import_line="from data_science import Pandas, NumPy, PowerBI",
             tags="Pandas,NumPy,Matplotlib,Seaborn,Power BI,Jupyter", sort_order=6),
        dict(category="Backend & APIs",
             import_line="from backend import Django, Flask, RESTAPI",
             tags="Django,Flask,REST APIs,Microservices,Model Serving", sort_order=7),
        dict(category="Databases & Tools",
             import_line="from tools import Git, MySQL, SQLite, Copilot",
             tags="MySQL,SQLite,Git,GitHub/GitLab,VS Code,Cursor,GitHub Copilot,Zapier", sort_order=8),
    ]
    for sg in skill_groups:
        db.session.add(SkillGroup(**sg))

    projects = [
        dict(name="CodeGuardian AI", file="codeguardian_ai.py", period="In Progress",
             description=("AI-powered Python code review, bug detection and auto-fix "
                           "platform. Django-based, built against a 16-week roadmap "
                           "targeting an MVP, a beta and a public launch."),
             tech="Django,Python,LLMs,Static Analysis,REST API",
             github="https://github.com/Arshdeep6840/CodeGuardian_AI",
             live="", highlight=True, sort_order=1),
        dict(name="HireSense AI", file="hiresense_ai.py", period="Apr 2026 – May 2026",
             description=("End-to-end AI recruitment platform. Semantic candidate "
                           "matching and resume screening with Sentence Transformers, "
                           "LLM-driven interview feedback generation, and audio-based "
                           "interview analysis with Librosa — all behind a modular "
                           "Django REST API."),
             tech="Django,REST API,Hugging Face,Sentence Transformers,LLMs,JavaScript",
             github="https://github.com/Arshdeep6840/Hire-sense-AI-",
             live="", highlight=True, sort_order=2),
        dict(name="IntellTrade AI", file="intelltrade_ai.py", period="Feb 2026 – Mar 2026",
             description=("AI-driven trading analytics platform with live market data "
                           "ingestion. ARIMA, LSTM and Prophet models forecast price "
                           "trends, exposed through REST endpoints and rendered on an "
                           "interactive portfolio-analytics dashboard."),
             tech="Python,REST API,ARIMA,LSTM,Prophet,Pandas",
             github="https://github.com/Arshdeep6840/IntellTrade-AI-",
             live="", highlight=True, sort_order=3),
        dict(name="House Price Prediction", file="house_price_prediction.py", period="Machine Learning",
             description=("Ensemble regression model (Random Forest + Gradient Boosting "
                           "+ XGBoost) tuned with GridSearchCV, reaching 99.5% test "
                           "accuracy. Shipped as an interactive Streamlit app with "
                           "Lottie animations."),
             tech="Python,Scikit-learn,XGBoost,Streamlit,Pandas",
             github="https://github.com/Arshdeep6840/House-Price-Prediction-Using-Machine-Learning",
             live="", highlight=False, sort_order=4),
    ]
    for p in projects:
        db.session.add(Project(**p))

    experience = [
        dict(role="Data Science Intern", org="Unified Mentor", period="Apr 2025 – May 2025",
             commit="a3f9c1e", sort_order=1,
             points=(
                 "Built classification and regression models with Python and Scikit-Learn on real-world datasets.\n"
                 "Ran data cleaning, EDA, feature engineering and evaluation with accuracy, precision, recall and F1-score.\n"
                 "Delivered automated visual reports in Matplotlib/Seaborn to communicate trends and model insights."
             )),
        dict(role="Data Science Using Python Trainee", org="CETPA Infotech", period="Jan 2025 – Apr 2025",
             commit="7bd21a4", sort_order=2,
             points=(
                 "Developed ML/DL models and deployed selected outputs via Django/Flask REST APIs.\n"
                 "Built preprocessing pipelines: missing-value handling, encoding, scaling, train-test splitting.\n"
                 "Automated workflow tasks with Zapier and Python scripts across Agile-style learning cycles."
             )),
    ]
    for e in experience:
        db.session.add(Experience(**e))

    education = [
        dict(degree="Master of Computer Applications (MCA)", school="Guru Nanak College, Budhlada",
             period="2025 – 2027", detail="", link="https://gncbudhlada.com/", sort_order=1),
        dict(degree="Bachelor of Vocational — Software Development", school="Guru Nanak College, Budhlada",
             period="2022 – 2025", detail="CGPA: 8.7", link="https://gncbudhlada.com/", sort_order=2),
        dict(degree="Class XII", school="Punjab Board", period="2021", detail="77%", link="", sort_order=3),
        dict(degree="Class X", school="Punjab Board", period="2019", detail="71%", link="", sort_order=4),
    ]
    for ed in education:
        db.session.add(Education(**ed))

    certifications = [
        dict(name="Data Science Intern", company="Unified Mentor", image="", sort_order=1),
        dict(name="Certificate Course in Artificial Intelligence & Data Science",company = "Cetpa Infotech Pvt. Ltd", image="", sort_order=2),
    ]
    for cert in certifications:
        db.session.add(Certification(**cert))

    # Matches the DOCUMENTS structure you provided. Actual files (PDF, PPTX,
    # DOCX, MP4) aren't included here since I don't have the binaries — go to
    # /admin/resources/ and upload each file + preview thumbnail once, and
    # size_label will auto-fill from the uploaded file.
    resources = [
        dict(title="AI Analyst Handbook", resource_type="pdf",
             description="Complete beginner guide to Agentic AI.",
             category="", content="", external_url="", file_path="", preview_image="",
             size_label="", duration_label="", sort_order=1),
        dict(title="AI Portfolio Presentation", resource_type="ppt",
             description="Presentation used during interviews.",
             category="", content="", external_url="", file_path="", preview_image="",
             size_label="", duration_label="", sort_order=2),
        dict(title="Resume", resource_type="docx",
             description="Latest ATS-friendly resume.",
             category="", content="", external_url="", file_path="", preview_image="",
             size_label="", duration_label="", sort_order=3),
        dict(title="Project Demo", resource_type="video",
             description="Complete walkthrough of the AI project.",
             category="", content="", external_url="", file_path="", preview_image="",
             size_label="", duration_label="4 min 12 sec", sort_order=4),
    ]
    for r in resources:
        db.session.add(Resource(**r))

    db.session.commit()


if __name__ == "__main__":
    # create_app() already seeds automatically if the DB is empty.
    from app import create_app
    create_app()
    print("Seed complete (or already seeded).")
