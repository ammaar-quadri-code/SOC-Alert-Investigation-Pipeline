import json

with open("../alerts/alert1.json") as file:
    data = json.load(file)

print("===== Analyst Summary =====")
print()

print("Rule:", data.get("rule"))
print("User:", data.get("user"))
print("Host:", data.get("host"))
print("Process:", data.get("process"))
print("Severity:", data.get("severity"))

print()
print("Evidence:")
print("- Encoded PowerShell execution detected")

print()
print("Recommended Actions:")
print("- Review PowerShell logs")
print("- Check parent process")
print("- Investigate source IP")