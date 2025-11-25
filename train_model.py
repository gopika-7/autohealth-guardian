# src/train_model.py

import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import joblib


# ----------------------------------------
# CORRECT PATHS FOR YOUR PROJECT
# ----------------------------------------
BASE_DIR = Path(__file__).resolve().parent      # src/
DATA_DIR = BASE_DIR / "data"                    # src/data/
USER_FILE = DATA_DIR / "user_1.json"            # src/data/user_1.json
MODEL_PATH = DATA_DIR / "model_dehydration.joblib"


# ----------------------------------------
# Load Telemetry JSON
# ----------------------------------------
def load_telemetry(path: Path):
    if not path.exists():
        print(f"❌ ERROR: Telemetry file not found: {path}")
        return None

    obj = json.loads(path.read_text())

    user_key = next(iter(obj.keys()))
    rows = obj[user_key]["telemetry"]

    df = pd.DataFrame(rows)

    if "ts" in df.columns:
        df["ts"] = pd.to_datetime(df["ts"])

    return df


# ----------------------------------------
# Feature Engineering
# ----------------------------------------
def prepare_features(df: pd.DataFrame):
    df = df.copy()

    df["water_ml"] = pd.to_numeric(df["water_ml"], errors="coerce").fillna(0)
    df["steps"] = pd.to_numeric(df["steps"], errors="coerce").fillna(0)
    df["sleep_hours"] = pd.to_numeric(df["sleep_hours"], errors="coerce").fillna(0)
    df["screen_minutes"] = pd.to_numeric(df["screen_minutes"], errors="coerce").fillna(0)

    df["dehydration"] = (df["water_ml"] < 1200).astype(int)

    X = df[["steps", "sleep_hours", "screen_minutes", "water_ml"]]
    y = df["dehydration"]

    return X, y, df


# ----------------------------------------
# Train + Save Model
# ----------------------------------------
def train_model():
    print("📥 Loading telemetry:", USER_FILE)

    df = load_telemetry(USER_FILE)
    if df is None:
        print("❌ Training aborted — telemetry file missing.")
        return

    print(f"📊 Loaded {len(df)} rows")

    X, y, df_full = prepare_features(df)

    if len(df_full) < 5:
        print("⚠ Warning: very small dataset — add more data for accuracy.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    print("🤖 Training Logistic Regression model...")
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]

    print("\n📈 Classification Report:")
    print(classification_report(y_test, y_pred))

    try:
        auc = roc_auc_score(y_test, y_proba)
        print(f"AUC Score: {auc:.3f}")
    except:
        print("AUC could not be calculated.")

    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump({"model": clf}, MODEL_PATH)

    print("\n💾 Model saved to:", MODEL_PATH)
    print("✅ Training complete!")


# ----------------------------------------
# Run directly
# ----------------------------------------
if __name__ == "__main__":
    train_model()
