
import pandas as pd
import pickle
from datetime import datetime
import json

# CONFIG
MODEL_PATH = "model.pkl"
POWER_LOG_FILE = "power_log.csv"
RECOMMENDATION_FILE = "recommendations.json"

# Load trained model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Load and preprocess power data
def extract_features(df):
    avg_voltage = df['voltage'].mean()
    avg_current = df['current'].mean()
    avg_power = df['power'].mean()
    hour = datetime.now().hour
    return [[avg_voltage, avg_current, avg_power, hour]]

def make_prediction(features):
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features).max()
    return prediction, round(proba, 2)

# Main execution
try:
    df = pd.read_csv(POWER_LOG_FILE)
    df = df.tail(60)  # last 60 seconds
    features = extract_features(df)
    decision, confidence = make_prediction(features)

    result = {
        "timestamp": datetime.now().isoformat(),
        "decision": decision,
        "confidence": confidence,
        "avg_voltage": features[0][0],
        "avg_current": features[0][1],
        "avg_power": features[0][2],
        "hour": features[0][3]
    }

    with open(RECOMMENDATION_FILE, "w") as f:
        json.dump(result, f, indent=4)

    print("AI decision:", decision, "Confidence:", confidence)

except Exception as e:
    print("Error:", e)
