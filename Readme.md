# AutoHealth Guardian

AutoHealth Guardian is a multi-agent personal health assistant demo built for the Kaggle Agents Intensive Capstone Project.

## What it does
- Ingests simulated health telemetry (steps, water, sleep, screen time)
- Runs risk detection and generates personalized advice
- Schedules reminders and logs notifications
- Stores long-term memory for trend analysis
- Generates a weekly PDF report

## Quickstart (local demo)
1. Clone the repo.
2. Create virtualenv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate


cd autohealth-guardian
python -m venv venv
venv\Scripts\activate
pip install pandas numpy joblib scikit-learn altair streamlit

pip install -r requirements.txt

cd D:\autohealth-guardian
python src/train_model.py or
.\.venv\Scripts\python.exe src/train_model.py        

streamlit run src/app.py


python src/simulate_data.py --user user_1 --days 14
python src/orchestrator.py --user user_1

python src/orchestrator.py
https://takeout.google.com/
for host
python -m src.train_model /
streamlit run streamlit_app.py  /
Option C — Run individual agents (for testing)
pip install reportlab


📱 How your phone reads the file
If your PC IP is 192.168.0.101, then the JSON will be accessible at:

http://192.168.0.101:8000/data/user_1.json
Example:

python src/agents/monitoring_agent.py


python src/tools/pdf_tool.py

pytest tests/test_agents.py

Get key:
https://home.openweathermap.org/api_keys  - weather api key
https://calorieninjas.com/profile - nutrition api key

autohealth-guardian/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ src/
│  ├─ agents/
│  ├─ tools/
│  ├─ orchestrator.py
│  └─ simulate_data.py
├─ notebooks/
└─ tests/
