import subprocess
import pathlib

BASE = pathlib.Path.home() / (
    ".openclaw/workspace-soc/skills/soc-toolkit/scripts"
)

WORKSPACE = pathlib.Path.home() / (
    ".openclaw/workspace-soc"
)

REPORT_FILE = WORKSPACE / "triage_input.txt"

print("Running SOC pipeline...")

# =====================================
# Run SOC Pipeline
# =====================================

pipeline = subprocess.run(
    ["python", str(BASE / "triage_pipeline.py")],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="ignore"
)

pipeline_output = pipeline.stdout

print("Pipeline completed.")

# =====================================
# Create Prompt
# =====================================

prompt = f"""
You are an SOC analyst.

Analyze this SOC pipeline output.

Generate:
- Severity
- Summary
- Threat explanation
- Threat intelligence analysis
- Recommendations

SOC PIPELINE OUTPUT:

{pipeline_output}
"""

# =====================================
# Save Prompt to File
# =====================================

REPORT_FILE.write_text(
    prompt,
    encoding="utf-8"
)

print("Prompt written to file.")

# =====================================
# OpenClaw Command
# =====================================

message = (
    "Read triage_input.txt from workspace "
    "and generate SOC triage analysis."
)

print("Sending request to OpenClaw...")

result = subprocess.run(
    [
        r"C:\Users\mhame\AppData\Roaming\npm\openclaw.cmd",
        "agent",
        "--agent",
        "soc-runner",
        "--message",
        message
    ],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="ignore"
)

print("OpenClaw response received.\n")

print(result.stdout)

if result.stderr:
    print("ERROR:")
    print(result.stderr)
