import json

with open("../alerts/alert1.json", "r") as file:
    data = json.load(file)

command = data.get("command", "")

if "EncodedCommand" in command:
    print("Suspicious PowerShell detected!")
    print("Severity:", data.get("severity"))
else:
    print("No suspicious behavior detected.")
