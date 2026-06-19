import json
import subprocess
import pathlib

BASE = pathlib.Path.home() / (
    ".openclaw/workspace-soc/skills/soc-toolkit/scripts"
)

ALERT_PATH = pathlib.Path.home() / (
    ".openclaw/workspace-soc/data/alerts/sim-powershell.json"
)

# ==========================================
# Helper Function
# ==========================================

def run_script(script_name, args=None, stdin_file=None):

    cmd = ["python", str(BASE / script_name)]

    if args:
        cmd.extend(args)

    result = subprocess.run(
        cmd,
        stdin=open(stdin_file, "r") if stdin_file else None,
        capture_output=True,
        text=True
    )

    try:
        return json.loads(result.stdout)
    except:
        return {
            "error": result.stderr
        }

# ==========================================
# 1. Normalize Alert
# ==========================================

normalized = run_script(
    "normalize_alert.py",
    stdin_file=ALERT_PATH
)

# ==========================================
# 2. Extract IOCs
# ==========================================

iocs = run_script(
    "extract_iocs.py",
    stdin_file=ALERT_PATH
)

# ==========================================
# 3. Sigma Match
# ==========================================

sigma = run_script(
    "sigma_match.py",
    stdin_file=ALERT_PATH
)

# ==========================================
# 4. Store Incident
# ==========================================

store = run_script(
    "incident_store.py",
    args=["append"],
    stdin_file=ALERT_PATH
)

# ==========================================
# 5. Enrich First IP
# ==========================================

enrichment = {}

if iocs.get("ips"):

    first_ip = iocs["ips"][0]

    enrichment = run_script(
        "enrich_ioc.py",
        args=[first_ip]
    )

# ==========================================
# Final SOC Report
# ==========================================

report = {
    "normalized_alert": normalized,
    "iocs": iocs,
    "sigma_matches": sigma,
    "incident_store": store,
    "enrichment": enrichment
}

print(json.dumps(report, indent=2))