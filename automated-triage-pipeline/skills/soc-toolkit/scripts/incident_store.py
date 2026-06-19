import json
import sys
import pathlib
import datetime

root = pathlib.Path.home() / ".openclaw/workspace-soc/data/incidents"

root.mkdir(parents=True, exist_ok=True)

path = root / (
    datetime.datetime.now(datetime.UTC).strftime("%Y-%m") + ".jsonl"
)

action = sys.argv[1]

try:

    if action == "append":

        doc = json.load(sys.stdin)

        doc["stored_at"] = (
            datetime.datetime.now(datetime.UTC).isoformat()
        )

        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(doc) + "\n")

        print(json.dumps({
            "ok": True,
            "path": str(path)
        }))

    elif action == "search":

        needle = sys.argv[2].lower()

        hits = []

        for file in sorted(root.glob("*.jsonl")):

            for line in file.read_text(
                encoding="utf-8"
            ).splitlines():

                if needle in line.lower():
                    hits.append(json.loads(line))

        print(json.dumps({
            "hits": hits[:20]
        }, indent=2))

    else:

        print(json.dumps({
            "error": "Invalid action"
        }))

except Exception as e:

    print(json.dumps({
        "error": str(e)
    }))