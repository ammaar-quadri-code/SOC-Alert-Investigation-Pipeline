import json
import sys

alert = json.load(sys.stdin)

matches = []

# ==================================================
# Suspicious PowerShell
# ==================================================

command = alert.get("command_line", "")

if "-EncodedCommand" in command:
    matches.append({
        "rule": "Suspicious PowerShell",
        "severity": "high"
    })

# ==================================================
# Multiple Failed Logins
# ==================================================

if alert.get("failed_attempts", 0) > 5:
    matches.append({
        "rule": "Multiple Failed Logins",
        "severity": "medium"
    })

# ==================================================
# Login From Unusual Location
# ==================================================

country = alert.get("country")
usual_country = alert.get("usual_country")

if (
    country
    and usual_country
    and country != usual_country
):
    matches.append({
        "rule": "Login From Unusual Location",
        "severity": "high"
    })

# ==================================================
# Suspicious File Download
# ==================================================

url = alert.get("url", "").lower()

if (
    ".exe" in url
    or ".dll" in url
    or ".bat" in url
    or ".ps1" in url
):
    matches.append({
        "rule": "Suspicious File Download",
        "severity": "medium"
    })

# ==================================================
# Connection To Suspicious IP
# ==================================================

bad_ips = [
    "185.220.101.1",
    "45.10.20.1",
    "103.44.22.1"
]

destination_ip = alert.get("destination_ip")

if destination_ip in bad_ips:
    matches.append({
        "rule": "Connection To Suspicious IP",
        "severity": "high"
    })

# ==================================================
# Web Attack Attempt
# ==================================================

url = alert.get("url", "")

if (
    "' OR 1=1" in url
    or "../" in url
    or "<script>" in url.lower()
):
    matches.append({
        "rule": "Web Attack Attempt",
        "severity": "high"
    })

# ==================================================
# Malware-like Process Execution
# ==================================================

suspicious_processes = [
    "rundll32.exe",
    "mimikatz.exe",
    "psexec.exe",
    "wmic.exe"
]

process = alert.get("process", "").lower()

if process in suspicious_processes:
    matches.append({
        "rule": "Malware-like Process Execution",
        "severity": "high"
    })

# ==================================================
# Privilege Escalation Attempt
# ==================================================

action = alert.get("action", "")

if (
    "Administrators" in action
    or "sudo" in action.lower()
):
    matches.append({
        "rule": "Privilege Escalation Attempt",
        "severity": "high"
    })

# ==================================================
# Cloud Misconfiguration
# ==================================================

if alert.get("public_access") is True:
    matches.append({
        "rule": "Cloud Misconfiguration",
        "severity": "medium"
    })

# ==================================================
# Data Exfiltration Simulation
# ==================================================

if alert.get("bytes_sent", 0) > 1000000000:
    matches.append({
        "rule": "Data Exfiltration Simulation",
        "severity": "critical"
    })

# ==================================================
# Output
# ==================================================

print(json.dumps({
    "matched_rules": matches
}, indent=2))