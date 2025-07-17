
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

def plot_power_log():
    try:
        df = pd.read_csv("power_log.csv")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)

        plt.figure(figsize=(12, 6))
        plt.plot(df["power"], label="Power (W)", linewidth=2)
        plt.title("Power Consumption Over Time")
        plt.xlabel("Time")
        plt.ylabel("Power (W)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig("power_log_plot.png")
        print("Power log plot saved as power_log_plot.png")
    except Exception as e:
        print("Error plotting power log:", e)

def show_latest_recommendation():
    try:
        with open("recommendations.json", "r") as f:
            rec = json.load(f)
        print("\nLatest AI Recommendation:")
        print(json.dumps(rec, indent=4))
    except Exception:
        print("No recommendation found.")

def show_override_log():
    try:
        with open("override_log.json", "r") as f:
            overrides = json.load(f)
        print("\nRecent User Overrides:")
        for entry in overrides[-5:]:  # Show last 5
            print(entry)
    except Exception:
        print("No override log found.")

if __name__ == "__main__":
    plot_power_log()
    show_latest_recommendation()
    show_override_log()
