import json
import os
import sys
import requests

from dotenv import load_dotenv

# Load environment variables
load_dotenv(
    os.path.expanduser(
        "~/.openclaw/workspace-soc/.env.local"
    )
)

# IOC from terminal argument
ioc = sys.argv[1]

result = {
    "ioc": ioc,
    "providers": {}
}

try:

    # ====================================
    # AbuseIPDB
    # ====================================

    abuse_key = os.getenv("ABUSEIPDB_API_KEY")

    if abuse_key:

        abuse_response = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            headers={
                "Key": abuse_key,
                "Accept": "application/json"
            },
            params={
                "ipAddress": ioc,
                "maxAgeInDays": 30
            },
            timeout=10
        )

        result["providers"]["abuseipdb"] = {
            "status": abuse_response.status_code,
            "body": abuse_response.json()
        }

    # ====================================
    # VirusTotal
    # ====================================

    vt_key = os.getenv("VT_API_KEY")

    if vt_key:

        vt_response = requests.get(
            f"https://www.virustotal.com/api/v3/ip_addresses/{ioc}",
            headers={
                "x-apikey": vt_key,
                "accept": "application/json"
            },
            timeout=10
        )

        result["providers"]["virustotal"] = {
            "status": vt_response.status_code,
            "body": vt_response.json()
        }

    # ====================================
    # AlienVault OTX
    # ====================================

    otx_key = os.getenv("OTX_API_KEY")

    if otx_key:

        otx_response = requests.get(
            f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ioc}/general",
            headers={
                "X-OTX-API-KEY": otx_key
            },
            timeout=10
        )

        result["providers"]["otx"] = {
            "status": otx_response.status_code,
            "body": otx_response.json()
        }

    # Final result
    print(json.dumps(result, indent=2))

except Exception as e:

    print(json.dumps({
        "error": str(e)
    }))