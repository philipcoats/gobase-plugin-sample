<!-- A copy of https://take66.ai/gobase/agent-spec, so agents can read it offline. That page is the one kept current. -->


GoBase is a to-do list of what needs you, drawn from the apps and services you use. This page tells an AI agent how to build a card for it. Give your agent this prompt:

> Read the spec at https://take66.ai/gobase/agent-spec and build a GoBase card that shows: [what you want on it].

## If you are the agent

A GoBase card is a small JSON file that you write into a folder. GoBase reads the file and draws the card. GoBase never runs anything from it and never writes back to your data source.

1. Ask the user what should need their attention, and where that information comes from.
2. Write a small script or app that gets the data and writes the JSON file described below.
3. Ask the user before you install anything that runs on a schedule.
4. Read the feedback file GoBase writes, and fix any errors or warnings.
5. Tell the user to press **+** on a GoBase dashboard, open the **Custom** tab, and add the card from there. A new card doesn't appear on a dashboard by itself. (Cards from other apps and agents are listed under Custom; the Take66 tab is only for Take66's own apps and plug-ins.)

Never put passwords, API keys, tokens or codes in the file. Keep credentials where the user's system keeps them, such as Keychain.

## What makes a good card

Lead with what the user should act on. A failed build, a bill due tomorrow or a door left open belongs on a card. Set `urgency` so those rise to the top, and give each one a `link` to where it can be dealt with.

GoBase isn't a home screen or a set of widgets, so don't build a card that only displays information to glance at, such as weather or a clock. A card with nothing to report should say so with `emptyText` or a calm `health` message.

A card shows its first 3 items, then "Show more." Put the most important items first. Set `alwaysShow: true` on an item that should stay visible anyway, such as a total (up to 3 per card).

## Where the file goes

On a Mac:

```
~/Library/Mobile Documents/iCloud~ai~take66~gobase/Documents/Modules/v001/<id>.json
```

If `Modules` doesn't exist, GoBase isn't installed or hasn't started with iCloud on, so ask the user to open it. Create `v001` if only that part is missing. iCloud shares the file with the user's other devices.

Name the file after the card's `id`: `"id": "garage"` goes in `garage.json`. A file whose name and id differ is rejected.

An app in the App Sandbox, or one on iPhone or iPad, can't reach that path directly. Ask the user once to choose the GoBase folder with the standard folder picker, keep a security-scoped bookmark to it, and write to `Modules/v001` inside it.

## The smallest card

```json
{ "schema": 2, "id": "garage", "name": "Garage door",
  "items": [ { "id": "door", "title": "Garage door is open", "urgency": "high" } ] }
```

## Card fields

| Field | Required | Meaning |
|---|---|---|
| `schema` | yes | Always `2`. |
| `id` | yes | Stable, up to 64 characters: lowercase letters, digits, `-`, `_` or `.`, not starting with `.`. Don't start it with `gobase.`, which is reserved. GoBase doesn't lowercase it for you, and a card with any other id can't be encrypted. |
| `name` | yes | The card's title, up to 80 characters. |
| `items` | yes | The rows, up to 200. |
| `icon` | no | An SF Symbol name. |
| `description` | no | One or two sentences about the card. |
| `homeLink` | no | Where the card's title button goes. |
| `privacy` | no | One plain sentence on what the card shares. |
| `generatedAt` | no | ISO 8601 time the data was made. Defaults to the file's modified time. |
| `staleAfter` | no | Seconds after `generatedAt` when GoBase should show the data as out of date. Leave it out if the data only changes when the user acts. |
| `expectedUpdate` | no | ISO 8601 time you expect to write next. |
| `health` | no | `{ "state": "ok", "message": "All good" }`. State is `ok`, `attention`, `error` or `setup-needed`. |
| `badge` | no | The one number that needs the user, shown on the card's sidebar icon. |
| `actionItems` | no | The card's lines on the dashboard's Summary: `[{ "text": "3 builds failed" }]`, up to 10, each up to 200 characters. Add `"link"` to an entry to make its open icon go there, `"value"` for a count, and `"lines"` for up to 10 smaller text lines under it. Summary always shows every entry, after the card's name in bold. One link per entry: two things to open means two entries. `[]` means no lines. Leave it out and GoBase shows one line from `health`. |
| `emptyText` | no | What to show when there are no items. |
| `columns` | no | Column titles for a table. See below. |
| `writtenBy` | no | `{ "app": "My script", "device": "Mac mini" }`. |

## Item fields

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Stable across updates. It's how GoBase remembers what was dismissed. |
| `title` | yes | The main line, up to 120 characters. |
| `kind` | no | `todo` (the default), `summary`, `stat` or `notification`. |
| `summary` | no | Plain text on the title's line, up to 240 characters. With it, the title is bold. |
| `detail` | no | The second line, up to 240 characters. |
| `info` | no | Longer plain text, up to 2,000 characters, shown when the row is clicked. Line breaks are kept. |
| `urgency` | no | `none`, `low`, `normal` (the default), `high` or `urgent`. Rows are ordered by this. |
| `due` | no | A date or ISO 8601 date-time. |
| `occurredAt` | no | ISO 8601 time it happened. |
| `value` | for `stat` | A number or short text. On a row with a `summary` or `lines`, it shows as a count. |
| `lines` | no | Up to 10 smaller text-only lines under the row, each up to 240 characters. They can't have links: a row has one `link`, so two things to open means two items. |
| `icon` | no | An SF Symbol name. |
| `link` | no | Where the row's open button goes. |
| `dismissible` | no | `true` lets the user dismiss it in GoBase. It comes back if you change the item. |
| `format` | no | Keywords that style the title: `bold`, `italic`, `underline`, `strikethrough`, `muted`, or one color (`red`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `gray`). For example `"bold red"`. Use sparingly. |
| `alwaysShow` | no | `true` keeps it visible when the card shows only its first 3 items. Up to 3 per card. |
| `cells` | no | Table values. See below. |

## Tables

Add `columns` to show rows as a table. Give 2 to 5 titles. The first is the column for each item's `title`, and each item's `cells` holds one value for every other column, in order.

```json
{ "schema": 2, "id": "my-builds", "name": "Builds", "columns": ["Project", "Mac", "iOS"],
  "items": [ { "id": "app-one", "kind": "summary", "title": "App One", "detail": "iOS build failed",
               "urgency": "high", "info": "Mac: 1.2 (40), Nov 9\niOS: build 41 failed",
               "cells": [ { "text": "1.2 (40)", "detail": "Nov 9", "tone": "good" },
                          { "text": "Failed", "detail": "Build 41", "tone": "problem" } ] } ] }
```

A cell is `{ "text", "detail", "tone" }` or just a string. `tone` is `muted`, `good`, `info`, `warning` or `problem`, and only what matters should have color. Keep cells to a few words, because a card is about 500 points wide. Always include `title` and `detail` too: narrow screens show ordinary rows made from them.

## Links

Use `https://`, `mailto:`, or an app's own link scheme. The user is asked the first time a card opens another app. These are never opened: `file`, `javascript`, `data`, `about`, `blob`, `shortcuts`, `workflow`, `x-callback-url`, and file-server or remote-login schemes such as `smb`, `afp`, `ftp`, `ssh` and `vnc`.

## Writing the file

- Write only your own file, and only when something has changed, at most about once a minute.
- Write atomically: a temporary file in the same folder, with a name starting with `.` so GoBase ignores it, then rename it.
- Write from one device only.
- Keep the whole file under 256 KB.
- All text is plain text.

GoBase checks the folder about every 30 seconds. To update it at once on a Mac, run `notifyutil -p ai.take66.gobase.module-updated`.

## Check your work

GoBase writes `<id>.status.json` beside your file with whether it was accepted and every error and warning, with the field each one applies to. Read it after GoBase has seen your file. Unknown fields are ignored and reported, and one bad item is skipped without blanking the card. A file is rejected only if it isn't JSON, has no `id` or `name`, or is over the limits.

## A complete example

A Mac script. Run it by hand first, and ask the user before scheduling it, for example with launchd.

```python
#!/usr/bin/env python3
import json, os, tempfile
from datetime import datetime, timezone
from pathlib import Path

CARD_ID = "disk-space"
FOLDER = Path.home() / "Library/Mobile Documents/iCloud~ai~take66~gobase/Documents/Modules/v001"

stats = os.statvfs("/")
free_gb = stats.f_bavail * stats.f_frsize / 1_000_000_000
items = []
if free_gb < 50:
    items.append({"id": "low-disk", "title": "Disk space is low",
                  "detail": f"{free_gb:.0f} GB free", "urgency": "high" if free_gb < 15 else "normal"})

card = {"schema": 2, "id": CARD_ID, "name": "Disk space", "icon": "internaldrive",
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "staleAfter": 7200, "emptyText": "Plenty of disk space",
        "health": {"state": "attention" if items else "ok"},
        "writtenBy": {"app": "Disk space script"}, "items": items}

FOLDER.mkdir(parents=True, exist_ok=True)
handle, temporary = tempfile.mkstemp(dir=FOLDER, prefix=".tmp-")
with os.fdopen(handle, "w") as file:
    json.dump(card, file, indent=2)
os.replace(temporary, FOLDER / f"{CARD_ID}.json")
```

## Optional: encrypt the file

Other apps with access to the folder can read a plain file. For anything private, encrypt it so only GoBase can read it.

1. Ask the user to press **+** on a GoBase dashboard, open **Custom**, choose **Connect Another App…**, type your card id, and click **Create and Copy Key**. The card doesn't have to exist yet. Your program can also open `gobase://connect/<your id>` to bring up that page (put only the id in the link, never a key).
2. Have the user paste the key into your program. Keep it in Keychain, and let them paste a new one later.
3. Write only the sealed form from then on. GoBase refuses plain files for a card that has a key. The card goes on that dashboard when your first file arrives.

The key is `gobase-key-1:` followed by base64url of GoBase's X25519 public key (32 bytes), your card's shared bytes (32 bytes), and your card id (UTF-8).

Seal with HPKE (RFC 9180) in PSK mode, suite X25519 / HKDF-SHA256 / ChaCha20-Poly1305. The recipient key is GoBase's public key, info is `GoBase module v1`, the pre-shared key is the shared bytes, the PSK id is your card id, and the authenticated data is your card id. Encrypt your normal JSON. Write this as `<id>.json`:

```json
{ "schema": 2, "id": "<id>", "encrypted": { "v": 1, "enc": "<base64 encapsulated key>", "ct": "<base64 ciphertext>" } }
```

To disconnect, stop writing, then write the card one last time, sealed, with `"disconnected": true`, `"items": []` and `generatedAt` set to now. Then delete the key, and keep the file. GoBase shows the card as disconnected until a newer file arrives.

The status file is then encrypted too: `{ "moduleID": "<id>", "encrypted": { "v": 1, "box": "<base64>" } }`. The box is ChaCha20-Poly1305 combined (nonce, ciphertext, tag). Its key is HKDF-SHA256 of your shared bytes with info `GoBase status v1` and 32 bytes of output, and the authenticated data is your card id.

