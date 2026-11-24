#!/usr/bin/env python3
"""GoBase card: warns when the Mac's disk is getting full.

Run:  python3 disk_space.py            (writes the card into GoBase's folder)
      python3 disk_space.py --dry-run  (prints the card instead)
Format: https://take66.ai/gobase/agent-spec
"""
import json, os, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

CARD_ID = "disk-space"            # lowercase letters, digits, - _ . ; the file is <id>.json
WARN_BELOW_GB = 50                # show an item below this
URGENT_BELOW_GB = 15              # and make it urgent below this

# GoBase's folder in iCloud Drive. GOBASE_FOLDER overrides it (handy for testing).
FOLDER = Path(os.environ.get("GOBASE_FOLDER") or
              Path.home() / "Library/Mobile Documents/iCloud~ai~take66~gobase/Documents/Modules/v001")


def build_card():
    stats = os.statvfs("/")
    free_gb = stats.f_bavail * stats.f_frsize / 1_000_000_000
    items = []
    if free_gb < WARN_BELOW_GB:
        items.append({
            "id": "low-disk",
            "title": "Disk space is low",
            "detail": f"{free_gb:.0f} GB free",
            "urgency": "urgent" if free_gb < URGENT_BELOW_GB else "high",
            "link": "x-apple.systempreferences:com.apple.settings.Storage",
        })
    return {
        "schema": 2,
        "id": CARD_ID,
        "name": "Disk space",
        "icon": "internaldrive",
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "staleAfter": 7200,
        "emptyText": f"Plenty of space: {free_gb:.0f} GB free",
        "health": {"state": "attention" if items else "ok"},
        "actionItems": [{"text": f"Disk: {free_gb:.0f} GB free"}] if items else [],
        "writtenBy": {"app": "Disk space script"},
        "items": items,
    }


def write_card(card):
    """Writes the card atomically, and only when something other than the time changed."""
    target = FOLDER / f"{card['id']}.json"
    if not FOLDER.parent.exists():
        sys.exit("GoBase's folder isn't there yet: open GoBase once with iCloud Drive on, then try again.")
    FOLDER.mkdir(exist_ok=True)
    try:
        old = json.loads(target.read_text())
        if {k: v for k, v in old.items() if k != "generatedAt"} == {k: v for k, v in card.items() if k != "generatedAt"}:
            return print("No change.")
    except (OSError, ValueError):
        pass
    handle, temporary = tempfile.mkstemp(dir=FOLDER, prefix=".tmp-")   # a "." name: GoBase ignores it
    with os.fdopen(handle, "w") as file:
        json.dump(card, file, indent=2)
    os.replace(temporary, target)
    subprocess.run(["notifyutil", "-p", "ai.take66.gobase.module-updated"], check=False)  # GoBase looks now
    print(f"Wrote {target}")


if __name__ == "__main__":
    card = build_card()
    if "--dry-run" in sys.argv:
        print(json.dumps(card, indent=2))
    else:
        write_card(card)
