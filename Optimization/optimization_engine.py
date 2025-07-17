
import csv
import time
from datetime import datetime

# === CONFIGURATION ===
CSV_LOG_FILE = "power_log.csv"
ALERT_LOG_FILE = "optimization_alerts.log"

# Thresholds (editable or configurable later)
MAX_CURRENT = 10.0     # Amps
MAX_POWER = 500.0      # Watts
MIN_VOLTAGE = 10.0     # Volts (for DC safety)
PEAK_HOURS = range(18, 22)  # 6 PM to 10 PM

# === Optimization Engine ===
def check_conditions(voltage, current, power, hour):
    alerts = []

    if current > MAX_CURRENT:
        alerts.append(f"⚠️ Overcurrent: {current:.2f}A")

    if power > MAX_POWER:
        alerts.append(f"⚠️ High power usage: {power:.2f}W")

    if voltage < MIN_VOLTAGE:
        alerts.append(f"⚠️ Low voltage detected: {voltage:.2f}V")

    if hour in PEAK_HOURS and power > 200:
        alerts.append(f"⚠️ Power usage during peak hours: {power:.2f}W")

    return alerts

# === Main Loop ===
def run_optimization():
    print("🔍 Running Optimization Engine (Press Ctrl+C to stop)...")
    try:
        while True:
            try:
                with open(CSV_LOG_FILE, "r") as file:
                    last_line = list(csv.reader(file))[-1]
                    timestamp, v, c, p = last_line
                    voltage = float(v)
                    current = float(c)
                    power = float(p)
                    hour = datetime.now().hour

                    alerts = check_conditions(voltage, current, power, hour)

                    if alerts:
                        print(f"[{timestamp}] Optimization Alerts:")
                        for alert in alerts:
                            print(" ", alert)
                        with open(ALERT_LOG_FILE, "a") as alert_log:
                            for alert in alerts:
                                alert_log.write(f"{timestamp} - {alert}\n")

            except Exception as e:
                print("Error reading log or processing data:", e)

            time.sleep(5)

    except KeyboardInterrupt:
        print("Optimization Engine stopped.")

if __name__ == "__main__":
    run_optimization()
