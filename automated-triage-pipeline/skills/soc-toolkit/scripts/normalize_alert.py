import json
import sys
import datetime

required = [
    "alert_id",
    "timestamp",
    "source",
    "rule",
    "severity"
]

try:
    doc = json.load(sys.stdin)

    missing = [k for k in required if k not in doc]

    if missing:
        raise Exception(f"Missing fields: {missing}")

    doc["severity"] = doc["severity"].lower()

    doc["normalized_at"] = (
        datetime.datetime.utcnow().isoformat() + "Z"
    )

    print(json.dumps(doc, indent=2))

except Exception as e:
    print(json.dumps({
        "error": str(e)
    }))
