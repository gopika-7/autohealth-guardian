📌 AutoHealth Guardian — AI Wellness Agent

AutoHealth Guardian is an AI-powered wellness assistant that analyzes daily telemetry such as hydration, steps, sleep hours, and screen time.
It predicts dehydration risk, computes wellness scores, and provides personalized insights.

This project is created as part of the Kaggle × Google AI Agents Intensive (Capstone Project).

🚀 Features
🔹 AI Agent (Gemini + ADK)

Uses tools

Uses context engineering

Supports memory

Generates actionable recommendations

🔹 Machine Learning Model

Logistic Regression

Predicts dehydration risk

Trains on telemetry signals

Saves model using Joblib

🔹 Streamlit Web Dashboard

Hydration analysis

Sleep tracking

Activity visualization

Stress estimates

Multi-risk prediction

Upload new telemetry JSON

One-click retraining button

🔹 Data Pipeline

JSON-based telemetry ingestion

Auto-cleaning

Auto-feature creation

Daily metrics extraction

🧠 Architecture Overview

(architecture diagram shown below)
<img src="architecture.png" width="650">

📊 Tech Stack
Purpose	Tools
Agent	Gemini 2.0 + ADK
ML Model	scikit-learn
Dashboard	Streamlit
Storage	JSON
Memory	ADK Memory
Charts	Altair
📁 Dataset

A 30-day telemetry dataset stored in:

src/data/user_1.json


Includes:

steps

water_ml

sleep_hours

screen_minutes

timestamps

🧪 Training

Train the model manually:

python src/train_model.py


Retrain from UI:

Click Run Training inside Streamlit

▶️ Run the Dashboard
streamlit run src/app.py


(Or for venv:)

.\.venv\Scripts\streamlit.exe run src/app.py

🌍 Deploy on Streamlit Cloud

Push repo to GitHub

Go to → https://share.streamlit.io

Select repo

Set file path to:

src/app.py


Add this to build:

pip install -r requirements.txt


Done. Your app is live!

                   ┌───────────────────────────┐
                   │        DATA SOURCE         │
                   │  (Kaggle Dataset / CSV)    │
                   └─────────────┬─────────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │   DATA LOADING        │
                     │ (Pandas / Notebook)   │
                     └───────────┬───────────┘
                                 │
                                 ▼
                ┌───────────────────────────────────┐
                │         DATA PREPROCESSING        │
                │ - Cleaning (NaN, duplicates)      │
                │ - Feature engineering             │
                │ - Encoding / Scaling              │
                └───────────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────┐
                     │   MODEL TRAINING        │
                     │ (RandomForest / XGB)    │
                     └──────────┬──────────────┘
                                │
                                ▼
                ┌───────────────────────────────────┐
                │          MODEL EVALUATION          │
                │ - Accuracy / RMSE / F1 Score       │
                │ - Validation                       │
                └──────────────────┬────────────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │   PREDICTION     │
                         │ (submission.csv) │
                         └──────────┬───────┘
                                    │
                                    ▼
                         ┌───────────────────────┐
                         │   KAGGLE SUBMISSION    │
                         │   Leaderboard score    │
                         └────────────────────────┘


🏆 Why This Project Fits the Kaggle Capstone

Uses AI Agent

Uses tools

Uses memory

Includes evaluation

Contains ML pipeline

Real dashboard + deployment

Clear architecture

Clean dataset

Practical real-world use case

📜 License

MIT License

🔥 PART 3 — Architecture Diagram (ASCII + Explanation)

Here is a clean, simple architecture diagram for your PNG file:

ARCHITECTURE DIAGRAM (Text Version)
                    ┌────────────────────────┐
                    │      User JSON Data     │
                    │   (30-day telemetry)    │
                    └───────────┬────────────┘
                                │
                                ▼
                   ┌──────────────────────────┐
                   │    Feature Engineering    │
                   │ steps, water, sleep, etc. │
                   └───────────┬──────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │  ML Model: LogisticRegression │
                 │  (train_model.py)             │
                 └───────────┬──────────────────┘
                                │
                                ▼
                    ┌───────────────────────────┐
                    │   model_dehydration.joblib│
                    └───────────┬──────────────┘
                                │
                                ▼
         ┌────────────────────────────────────────────────┐
         │                 Streamlit UI                    │
         │  - Dashboard (app.py)                           │
         │  - Charting (Altair)                            │
         │  - Upload JSON                                  │
         │  - Run Training                                 │
         └─────────────┬──────────────────────────────────┘
                        │
                        ▼
              ┌───────────────────────────┐
              │  Gemini ADK Agent          │
              │  - Tools                   │
              │  - Memory                  │
              │  - Recommendations         │
              └───────────────────────────┘



