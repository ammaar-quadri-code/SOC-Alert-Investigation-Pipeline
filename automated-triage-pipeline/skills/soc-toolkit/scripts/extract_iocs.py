import json
import re
import sys

try:
    doc = json.load(sys.stdin)

    blob = json.dumps(doc)

    ips = sorted(set(
        re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", blob)
    ))

    domains = sorted(set(
        re.findall(r"\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b", blob)
    ))

    hashes = sorted(set(
        re.findall(r"\b[a-fA-F0-9]{32,64}\b", blob)
    ))

    urls = sorted(set(
        re.findall(r"https?://[^\s]+", blob)
    ))

    result = {
        "ips": ips,
        "domains": domains,
        "hashes": hashes,
        "urls": urls
    }

    print(json.dumps(result, indent=2))

except Exception as e:
    print(json.dumps({
        "error": str(e)
    }))
