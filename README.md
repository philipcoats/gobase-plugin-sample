# Build your own GoBase card

[GoBase](https://take66.ai/gobase) shows cards of what needs you: mail, calendars, builds, and anything else you
connect. This repository is a starting point for building a card of your own, **with an AI agent doing the
building**. You don't need to know how to program.

Full instructions: https://take66.ai/gobase/build-your-own

## What a card is

A card is a small text file (JSON) that a script writes into GoBase's folder in iCloud Drive. GoBase reads it and
shows it on your dashboards, on your Mac, iPhone and iPad. GoBase never runs anything from the file and never
changes the thing it describes.

## Do it with an AI agent

1. Install an AI coding agent on your Mac: [Claude Code](https://claude.com/claude-code) (in the Claude app or the
   terminal) or [Codex](https://openai.com/codex).
2. Download this repository (**Code › Download ZIP**, then unzip it) or clone it, and open the folder in your agent.
3. Paste this prompt, with the parts in brackets filled in:

> I use GoBase, an app that shows cards of what needs my attention. Read AGENTS.md in this folder and the
> instructions at https://take66.ai/gobase/agent-spec, then build me a GoBase card that shows:
> **[what should need my attention, for example: "bills in my Bills spreadsheet that are due in the next two weeks"]**.
> The information comes from: **[where it lives, for example: "~/Documents/Bills.csv", "my Home Assistant", "a
> website I check every morning"]**. Update it **[how often, for example: every hour]**.
> Explain each step in plain words. Ask me before you install anything that runs on a schedule, and when you're
> done, tell me how to add the card in GoBase and how to remove what you installed.

4. Answer its questions. When it's done, in GoBase press **+** on a dashboard, open **Custom**, and add your card.

## Try the examples yourself

Each example runs with the `python3` that comes with Apple's developer tools (macOS asks to install them the first
time you type `python3` in Terminal).

```bash
python3 examples/disk-space/disk_space.py --dry-run      # prints the card
python3 examples/disk-space/disk_space.py                # writes it into GoBase's folder
python3 examples/bills-due/bills_due.py --dry-run
```

- **disk-space**: warns when the Mac's disk is getting full.
- **bills-due**: reads `bills.csv` and lists bills due soon, as a table, overdue ones first.

To run one on a schedule, see `schedule/README.md`.

## Remove a card

Delete its file from `~/Library/Mobile Documents/iCloud~ai~take66~gobase/Documents/Modules/v001/`, remove any
schedule you loaded (`schedule/README.md`), and remove the card from your dashboard in GoBase.

## Good to know

- Your card file syncs through **your** iCloud. Take66 doesn't see it, host it, review it or support it.
- Keep passwords and keys out of the card and the script; the agent will keep them in the Mac's Keychain.
- For anything private, ask your agent to encrypt the card so only GoBase can read it.

MIT License. © 2026 Take66 Software.
