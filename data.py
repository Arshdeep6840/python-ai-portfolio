# data.py

PROFILE = {
    "name": "Arshdeep Singh",
    "roles": [
        "AI/ML Engineer (1 YEAR)",
        "Python Developer (01 YEAR)"
    ],
    "location": "Mohali, Punjab, India",
    "email": "arshdeepsingh17092@gmail.com",
    "contact_number": "+91 6284519020",
    "github": "https://github.com/Arshdeep6840",
    "linkedin": "https://www.linkedin.com/in/arshdeep-singh-ai",
    "resume_file": "ARSHDEEP SINGH RESUME.PDF",
    "summary": (
        "AI/ML and Generative AI-focused Python developer who builds machine "
        "learning models, NLP workflows, LLM-powered applications and REST "
        "APIs end to end. Comfortable across the full stack of an AI "
        "product — data preprocessing and feature engineering, model "
        "training and serving, prompt engineering and RAG concepts, and "
        "shipping it behind a clean Django/Flask backend with a dashboard "
        "on top."
    ),
    "stats": [
        {"label": "AI/ML Projects Shipped", "value": "4+"},
        {"label": "Internships Completed", "value": "2"},
        {"label": "Core Skill Domains", "value": "8"},
        {"label": "Frameworks & Tools", "value": "20+"},
    ],
}

SKILLS = [
    dict(category="Programming",
         import_line="from languages import Python, SQL, JavaScript, HTML5, CSS3",
         tags="Python,SQL,JavaScript,HTML5,CSS3"),
    dict(category="AI / ML",
         import_line="from ml import Classification, Regression, FeatureEngineering",
         tags="Supervised Learning,Classification,Regression,Model Evaluation,Feature Engineering,Data Preprocessing"),
    dict(category="Deep Learning",
         import_line="from deep_learning import TensorFlow, Keras, CNN, LSTM",
         tags="TensorFlow,Keras,Neural Networks,LSTM,CNN Basics"),
    dict(category="Generative AI",
         import_line="from genai import LLMs, PromptEngineering, RAG",
         tags="LLMs,Prompt Engineering,Hugging Face Transformers,Sentence Transformers,RAG Concepts,AI API Integration"),
    dict(category="NLP",
         import_line="from nlp import NER, Embeddings, TextClassification",
         tags="NLTK,spaCy,Text Classification,Named Entity Recognition,Embeddings,Semantic Similarity"),
    dict(category="Data Science",
         import_line="from data_science import Pandas, NumPy, PowerBI",
         tags="Pandas,NumPy,Matplotlib,Seaborn,Power BI,Jupyter"),
    dict(category="Backend & APIs",
         import_line="from backend import Django, Flask, RESTAPI",
         tags="Django,Flask,REST APIs,Microservices,Model Serving"),
    dict(category="Databases & Tools",
         import_line="from tools import Git, MySQL, SQLite, Copilot",
         tags="MySQL,SQLite,Git,GitHub/GitLab,VS Code,Cursor,GitHub Copilot,Zapier"),
]

PROJECTS = [
    dict(name="CodeGuardian AI", file="codeguardian_ai.py", period="In Progress",
         description=("AI-powered Python code review, bug detection and auto-fix "
                       "platform. Django-based, built against a 16-week roadmap "
                       "targeting an MVP, a beta and a public launch."),
         tech="Django,Python,LLMs,Static Analysis,REST API",
         github="https://github.com/Arshdeep6840/CodeGuardian_AI",
         live="", highlight=True),
    dict(name="HireSense AI", file="hiresense_ai.py", period="Apr 2026 – May 2026",
         description=("End-to-end AI recruitment platform. Semantic candidate "
                       "matching and resume screening with Sentence Transformers, "
                       "LLM-driven interview feedback generation, and audio-based "
                       "interview analysis with Librosa — all behind a modular "
                       "Django REST API."),
         tech="Django,REST API,Hugging Face,Sentence Transformers,LLMs,JavaScript",
         github="https://github.com/Arshdeep6840/Hire-sense-AI-",
         live="", highlight=True),
    dict(name="IntellTrade AI", file="intelltrade_ai.py", period="Feb 2026 – Mar 2026",
         description=("AI-driven trading analytics platform with live market data "
                       "ingestion. ARIMA, LSTM and Prophet models forecast price "
                       "trends, exposed through REST endpoints and rendered on an "
                       "interactive portfolio-analytics dashboard."),
         tech="Python,REST API,ARIMA,LSTM,Prophet,Pandas",
         github="https://github.com/Arshdeep6840/IntellTrade-AI-",
         live="", highlight=True),
    dict(name="House Price Prediction", file="house_price_prediction.py", period="Machine Learning",
         description=("Ensemble regression model (Random Forest + Gradient Boosting "
                       "+ XGBoost) tuned with GridSearchCV, reaching 99.5% test "
                       "accuracy. Shipped as an interactive Streamlit app with "
                       "Lottie animations."),
         tech="Python,Scikit-learn,XGBoost,Streamlit,Pandas",
         github="https://github.com/Arshdeep6840/House-Price-Prediction-Using-Machine-Learning",
         live="", highlight=False),
]

EXPERIENCE = [

     dict(role = "AIML Trainer", org = "Solitaire Infosystem", period = "sep 2025 - Sep 2026",
     commit="",
     points=(
         "Provide training to students on AIML and Data Science.\n"
         "Hands on Projects\n"
         "Build the Resume with Projects"
     )),
    dict(role="Data Science Intern", org="Unified Mentor", period="Apr 2025 – May 2025",
         commit="a3f9c1e",
         points=(
             "Built classification and regression models with Python and Scikit-Learn on real-world datasets.\n"
             "Ran data cleaning, EDA, feature engineering and evaluation with accuracy, precision, recall and F1-score.\n"
             "Delivered automated visual reports in Matplotlib/Seaborn to communicate trends and model insights."
         )),
    dict(role="Data Science Using Python Trainee", org="CETPA Infotech", period="Jan 2025 – Apr 2025",
         commit="7bd21a4",
         points=(
             "Developed ML/DL models and deployed selected outputs via Django/Flask REST APIs.\n"
             "Built preprocessing pipelines: missing-value handling, encoding, scaling, train-test splitting.\n"
             "Automated workflow tasks with Zapier and Python scripts across Agile-style learning cycles."
         )),
]

EDUCATION = [
    dict(degree="Master of Computer Applications (MCA)", school="Guru Nanak College, Budhlada",
         period="2025 – 2027", detail="", link="https://gncbudhlada.com/"),
    dict(degree="Bachelor of Vocational — Software Development", school="Guru Nanak College, Budhlada",
         period="2022 – 2025", detail="CGPA: 8.7", link="https://gncbudhlada.com/"),
    dict(degree="Class XII", school="Punjab Board", period="2021", detail="77%", link=""),
    dict(degree="Class X", school="Punjab Board", period="2019", detail="71%", link=""),
]

CERTIFICATIONS = [
    dict(name="Data Science Intern", company="Unified Mentor", image=""),
    dict(name="Certificate Course in Artificial Intelligence & Data Science",company = "Cetpa Infotech Pvt. Ltd", image=""),
]


# Add to data.py
