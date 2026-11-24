# For AI agents (Claude Code, Codex and others)

The person who opened this folder wants a **GoBase card**: a small JSON file, written into GoBase's folder in iCloud
Drive, that GoBase shows as a card of what needs their attention. They are probably not a developer. Work in plain
words and keep what you build small.

1. Read the card format: https://take66.ai/gobase/agent-spec (a copy is in `docs/agent-spec.md`; the web page wins
   if they differ).
2. Ask what should need their attention and where that information comes from, if they haven't said.
3. Start from the closest example in `examples/` and copy it to a new folder; don't edit the examples in place.
   - `disk-space`: reads something on the Mac (no files, no accounts).
   - `bills-due`: reads a spreadsheet (CSV) and shows a table with due dates.
4. Run it by hand first. `--dry-run` prints the card instead of writing it.
5. Check GoBase's verdict in `<id>.status.json` beside the card file, and fix every error and warning.
6. Ask before scheduling anything. `schedule/` has a launchd template and the commands to load and remove it.
   Tell them exactly what you installed and how to remove it.
7. Tell them to add the card in GoBase: **+** on a dashboard › **Custom**. A new card doesn't appear by itself.

Rules:
- Never put passwords, API keys, tokens or codes in the card or in the script. If a service needs a key, keep it in
  the Mac's Keychain (`security add-generic-password` / `find-generic-password`) and have the person enter it.
- Read only. A card never changes or sends anything in the source it reads.
- Write only your own card file, atomically (a `.`-prefixed temp file, then rename), and only when something changed.
- If the card shows anything private (names, messages, amounts), offer to encrypt it (`docs/agent-spec.md` ›
  Optional: encrypt the file).
