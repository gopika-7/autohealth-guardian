import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.append(str(APP_DIR))

import streamlit as st
import json
import joblib
import altair as alt
import pandas as pd

from train_model import train_model

# ----------------------------------------
# FIXED PATHS (CORRECT FOR YOUR PROJECT)
# ----------------------------------------
BASE_DIR = Path(__file__).resolve().parent          # src/
DATA_DIR = BASE_DIR / "data"                        # src/data/
TELEMETRY_FILE = DATA_DIR / "user_1.json"           # src/data/user_1.json
MODEL_FILE = DATA_DIR / "model_dehydration.joblib"  # src/data/model...

# Debug info in UI
st.write("BASE_DIR:", BASE_DIR)
st.write("DATA_DIR:", DATA_DIR)
st.write("TELEMETRY FILE:", TELEMETRY_FILE)
st.write("Exists?", TELEMETRY_FILE.exists())

# ----------------------------------------
# Load telemetry JSON
# ----------------------------------------
if not TELEMETRY_FILE.exists():
    st.error(f"Missing file: {TELEMETRY_FILE}")
    st.stop()

with TELEMETRY_FILE.open() as f:
    obj = json.load(f)

user_key = next(iter(obj.keys()))
df = pd.DataFrame(obj[user_key]["telemetry"])
df["ts"] = pd.to_datetime(df["ts"])


# ----------------------------------------
# Capture console output
# ----------------------------------------
class OutputCapture(list):
    def write(self, msg):
        self.append(msg)

def run_with_capture(fn, *args, **kwargs):
    capture = OutputCapture()
    old_stdout = sys.stdout
    sys.stdout = capture
    try:
        result = fn(*args, **kwargs)
    finally:
        sys.stdout = old_stdout
    return result, "".join(capture)


# ----------------------------------------
# SIDEBAR CONTROLS
# ----------------------------------------
st.sidebar.header("Controls")
date_sel = st.sidebar.selectbox(
    "Select date to inspect",
    df['ts'].dt.date.astype(str).tolist()
)
window = st.sidebar.slider("Rolling window (days)", 3, 14, 7)
show_model = st.sidebar.checkbox("Load dehydration risk model", True)


# ----------------------------------------
# SUMMARY CARDS
# ----------------------------------------
col1, col2, col3, col4 = st.columns(4)
latest = df.iloc[-1]

col1.metric("Steps", int(latest['steps']))
col2.metric("Water (ml)", int(latest['water_ml']))
col3.metric("Sleep (hrs)", f"{latest['sleep_hours']:.1f}")
col4.metric("Screen (min)", int(latest['screen_minutes']))


# ----------------------------------------
# TIME SERIES CHARTS
# ----------------------------------------
st.markdown("---")
st.subheader("Time Series")

df['date'] = df['ts'].dt.date
df_sorted = df.set_index('ts').sort_index()
rolling = df_sorted[['steps', 'water_ml', 'sleep_hours', 'screen_minutes']] \
    .rolling(f"{window}D").mean().reset_index()

base = alt.Chart(df).encode(x='ts:T')

c1 = base.mark_line().encode(y='steps:Q').properties(height=200)
c2 = base.mark_line().encode(y='water_ml:Q').properties(height=200)
c3 = base.mark_line().encode(y='sleep_hours:Q').properties(height=200)
c4 = base.mark_line().encode(y='screen_minutes:Q').properties(height=200)

st.altair_chart((c1 & c2 & c3 & c4), use_container_width=True)


# ----------------------------------------
# SELECTED DAY DETAILS
# ----------------------------------------
st.markdown("---")
st.subheader("Selected Day Detail")

day_df = df[df['ts'].dt.date.astype(str) == date_sel]

if day_df.empty:
    st.warning("No data for selected date.")
else:
    st.write(day_df.iloc[0].to_dict())


# ----------------------------------------
# MODEL PREDICTIONS
# ----------------------------------------
if show_model:
    if not MODEL_FILE.exists():
        st.warning("Model file not found. Run training first.")
    else:
        bundle = joblib.load(MODEL_FILE)
        model = bundle["model"]

        X = df[['steps', 'sleep_hours', 'screen_minutes', 'water_ml']].fillna(0)
        df['dehydration_prob'] = model.predict_proba(X)[:, 1]

        st.subheader("Dehydration Risk (Model)")
        st.line_chart(df.set_index("ts")["dehydration_prob"])

        st.markdown("Top Risky Days:")
        st.table(
            df.sort_values('dehydration_prob', ascending=False)
              .head(5)
              .assign(ts=lambda d: d['ts'].dt.strftime("%Y-%m-%d"))
        )


# ----------------------------------------
# AGENT HEURISTICS
# ----------------------------------------
st.markdown("---")
st.subheader("Agent-Style Heuristics")

df['hydration_flag'] = (df['water_ml'] < 1200)
df['sleep_flag'] = (df['sleep_hours'] < 6)
df['low_activity'] = (df['steps'] < 3000)

st.write({
    "Low Water Days": int(df['hydration_flag'].sum()),
    "Low Sleep Days": int(df['sleep_flag'].sum()),
    "Low Activity Days": int(df['low_activity'].sum())
})


# ----------------------------------------
# UPLOAD JSON
# ----------------------------------------
st.markdown("## Upload Telemetry JSON")
uploaded = st.file_uploader("Upload JSON", type=["json"])
if uploaded:
    new = json.load(uploaded)
    st.success("Uploaded successfully!")
    st.json(new)


# ----------------------------------------
# MULTI-RISK
# ----------------------------------------
st.markdown("---")
st.subheader("Multi-Risk AI Predictions")

df["sleep_risk"] = 1 - (df["sleep_hours"] / 8).clip(0, 1)
df["low_activity_risk"] = (1 - (df["steps"] / 8000)).clip(0, 1)
df["stress_risk"] = (
    (df["screen_minutes"] / 300).clip(0, 1) * 0.6 +
    df["sleep_risk"] * 0.4
).clip(0, 1)

for title, col in {
    "Sleep Risk": "sleep_risk",
    "Activity Risk": "low_activity_risk",
    "Stress Risk": "stress_risk"
}.items():
    st.markdown(f"### {title}")
    st.line_chart(df.set_index("ts")[col])


# ----------------------------------------
# TRAIN MODEL LOGS
# ----------------------------------------
st.markdown("---")
st.subheader("🧪 Model Training Output")

if st.button("Run Training"):
    from train_model import train_model
    result, logs = run_with_capture(train_model)
    st.success("Training complete!")
    st.code(logs)
