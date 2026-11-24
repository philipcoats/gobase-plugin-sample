#!/usr/bin/env python3
"""GoBase card: bills from a spreadsheet (CSV) that are due soon, as a table, overdue first.

The CSV needs the columns Bill, Due (YYYY-MM-DD) and Amount; Paid (yes/no) and Link are optional.
Export one from Numbers or Excel with File › Export To › CSV, or point BILLS_FILE at your own.

Run:  python3 bills_due.py            (writes the card into GoBase's folder)
      python3 bills_due.py --dry-run  (prints the card instead)
Format: https://take66.ai/gobase/agent-spec
"""
import csv, json, os, subprocess, sys, tempfile
from datetime import date, datetime, timezone
from pathlib import Path

CARD_ID = "bills-due"
DAYS_AHEAD = 14
BILLS_FILE = Path(os.environ.get("BILLS_FILE") or Path(__file__).with_name("bills.csv"))
FOLDER = Path(os.environ.get("GOBASE_FOLDER") or
              Path.home() / "Library/Mobile Documents/iCloud~ai~take66~gobase/Documents/Modules/v001")


def when(days):
    if days < 0:
        return f"{-days} day{'s' if days != -1 else ''} overdue"
    return {0: "Today", 1: "Tomorrow"}.get(days, f"In {days} days")


def build_card(today=None):
    today = today or date.today()
    items = []
    with open(BILLS_FILE, newline="", encoding="utf-8-sig") as file:
        for n, row in enumerate(csv.DictReader(file)):
            name = (row.get("Bill") or "").strip()
            if not name or (row.get("Paid") or "").strip().lower() in ("yes", "y", "true", "x", "paid"):
                continue
            try:
                due = date.fromisoformat((row.get("Due") or "").strip())
            except ValueError:
                continue
            days = (due - today).days
            if days > DAYS_AHEAD:
                continue
            amount = (row.get("Amount") or "").strip()
            item = {
                "id": "bill-" + "".join(c for c in name.lower() if c.isalnum())[:40] or f"bill-{n}",
                "kind": "summary",
                "title": name,
                "detail": f"{when(days)} · ${amount}" if amount else when(days),
                "due": due.isoformat(),
                "urgency": "urgent" if days < 0 else "high" if days <= 3 else "normal",
                "cells": [
                    {"text": when(days), "tone": "problem" if days < 0 else "warning" if days <= 3 else "muted"},
                    f"${amount}" if amount else "",
                ],
            }
            if (row.get("Link") or "").startswith("https://"):
                item["link"] = row["Link"].strip()
            items.append((days, item))
    items = [i for _, i in sorted(items, key=lambda pair: pair[0])]
    overdue = sum(1 for i in items if i["urgency"] == "urgent")
    return {
        "schema": 2,
        "id": CARD_ID,
        "name": "Bills due",
        "icon": "dollarsign.circle",
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "staleAfter": 86400,
        "columns": ["Bill", "Due", "Amount"],
        "emptyText": f"No bills due in the next {DAYS_AHEAD} days",
        "health": {"state": "attention" if overdue else "ok",
                   "message": f"{overdue} overdue" if overdue else f"{len(items)} due soon"},
        "badge": overdue,
        "actionItems": [{"text": f"{len(items)} bill{'s' if len(items) != 1 else ''} due"
                                 + (f", {overdue} overdue" if overdue else "")}] if items else [],
        "privacy": "Bill names, due dates and amounts from your spreadsheet.",
        "writtenBy": {"app": "Bills due script"},
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
    handle, temporary = tempfile.mkstemp(dir=FOLDER, prefix=".tmp-")
    with os.fdopen(handle, "w") as file:
        json.dump(card, file, indent=2)
    os.replace(temporary, target)
    subprocess.run(["notifyutil", "-p", "ai.take66.gobase.module-updated"], check=False)
    print(f"Wrote {target}")


if __name__ == "__main__":
    card = build_card()
    if "--dry-run" in sys.argv:
        print(json.dumps(card, indent=2))
    else:
        write_card(card)
