import json

with open("../alerts/alert1.json") as file:
    alert = json.load(file)

with open("../intel/threat_intel.json") as file:
    intel = json.load(file)

ip = alert.get("src_ip")

print("Threat Intel Result")
print("--------------------")

if ip in intel:
    print(ip, "→", intel[ip])
else:
    print(ip, "→ Unknown")