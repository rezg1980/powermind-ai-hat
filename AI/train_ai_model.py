
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# Simulate data
samples = 500
np.random.seed(42)
avg_voltage = np.random.normal(12, 2, samples)
avg_current = np.random.normal(5, 1.5, samples)
avg_power = avg_voltage * avg_current + np.random.normal(0, 10, samples)
hour_of_day = np.random.randint(0, 24, samples)

labels = []
for p, h in zip(avg_power, hour_of_day):
    if p > 650:
        labels.append("shutdown")
    elif p < 60:
        labels.append("standby")
    else:
        labels.append("ok")

df = pd.DataFrame({
    "avg_voltage": avg_voltage,
    "avg_current": avg_current,
    "avg_power": avg_power,
    "hour_of_day": hour_of_day,
    "label": labels
})

X = df[["avg_voltage", "avg_current", "avg_power", "hour_of_day"]]
y = df["label"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
