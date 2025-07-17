
import RPi.GPIO as GPIO
import csv
import json
import time
from datetime import datetime

# === CONFIG ===
relay_pin_map = {
    "relay_1": 17,
    "relay_2": 27,
    "relay_3": 22
}

RULES_FILE = "control_rules_template.json"
DATA_FILE = "power_log.csv"

# === GPIO SETUP ===
GPIO.setmode(GPIO.BCM)
for pin in relay_pin_map.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Default OFF (HIGH for active-low relay)

def load_rules():
    with open(RULES_FILE, 'r') as f:
        return json.load(f)["rules"]

def read_latest_data():
    try:
        with open(DATA_FILE, 'r') as f:
            lines = f.readlines()
            if len(lines) < 2:
                return None
            last_line = lines[-1].strip().split(',')
            return {
                "timestamp": last_line[0],
                "voltage": float(last_line[1]),
                "current": float(last_line[2]),
                "power": float(last_line[3])
            }
    except Exception as e:
        print("Error reading data:", e)
        return None

def is_in_time_range(start, end):
    now = datetime.now().strftime('%H:%M')
    return start <= now <= end

def apply_rules(rules, data):
    for rule in rules:
        cond = rule["condition"]
        target = rule["target"]
        pin = relay_pin_map.get(target)
        if not pin:
            continue

        triggered = False

        if "power_greater_than" in cond and data["power"] > cond["power_greater_than"]:
            triggered = True
        if "voltage_less_than" in cond and data["voltage"] < cond["voltage_less_than"]:
            triggered = True
        if "time_range" in cond and is_in_time_range(cond["time_range"][0], cond["time_range"][1]):
            triggered = True
        if "optimization_recommendation" in cond:
            # Placeholder for future AI integration
            triggered = False

        if triggered:
            if rule["action"] == "turn_on":
                GPIO.output(pin, GPIO.LOW)
                print(f"[{datetime.now()}] ON → {target}")
            elif rule["action"] == "turn_off":
                GPIO.output(pin, GPIO.HIGH)
                print(f"[{datetime.now()}] OFF → {target}")
            elif rule["action"] == "turn_off_all":
                for p in relay_pin_map.values():
                    GPIO.output(p, GPIO.HIGH)
                print(f"[{datetime.now()}] ALL OFF")
