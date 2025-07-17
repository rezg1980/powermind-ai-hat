
import json
from datetime import datetime

# File paths
RECOMMENDATION_FILE = "recommendations.json"
OVERRIDE_LOG_FILE = "override_log.json"

def log_override(relay, action, user_reason="manual override"):
    try:
        # Load current AI recommendation
        with open(RECOMMENDATION_FILE, "r") as f:
            recommendation = json.load(f)
    except Exception:
        recommendation = {"decision": "unknown"}

    # Build override entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "relay": relay,
        "action": action,
        "ai_decision": recommendation.get("decision", "unknown"),
        "user_reason": user_reason
    }

    # Load existing log or create new
    try:
        with open(OVERRIDE_LOG_FILE, "r") as f:
            log = json.load(f)
    except:
        log = []

    log.append(entry)

    with open(OVERRIDE_LOG_FILE, "w") as f:
        json.dump(log, f, indent=4)

    print("Override logged:", entry)

# Example usage:
# log_override("relay_1", "ON", "needed lights")
