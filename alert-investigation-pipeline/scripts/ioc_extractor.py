import json

with open("../alerts/alert1.json", "r") as file:
    data = json.load(file)

print("IOC Extraction")
print("----------------")

print("IP Address:", data.get("src_ip"))
print("User:", data.get("user"))
print("Host:", data.get("host"))
print("Process:", data.get("process"))
