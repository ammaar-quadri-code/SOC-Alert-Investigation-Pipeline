import json

with open("../alerts/alert1.json", "r") as file:
    data = json.load(file)

required_fields = ["alert_id", "host", "user", "severity"]

missing = []

for field in required_fields:
    if field not in data:
        missing.append(field)

if missing:
    print("Missing fields:", missing)
else:
    print("Valid alert received.")