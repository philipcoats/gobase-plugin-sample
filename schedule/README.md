# Run a card on a schedule

macOS runs scheduled jobs with launchd. The template here runs a script every hour and when you log in.

1. Copy `ai.example.gobase-card.plist` to `~/Library/LaunchAgents/`, giving it your own name
   (for example `com.yourname.bills-due.plist`), and change its `Label` to the same name.
2. Change the script path to where your script is. Use the full path (no `~`).
3. Load it:

   ```bash
   launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.yourname.bills-due.plist
   ```

4. Check it ran: `launchctl print gui/$(id -u)/com.yourname.bills-due` and the log path in the file.

To stop it and remove it:

```bash
launchctl bootout gui/$(id -u)/com.yourname.bills-due
rm ~/Library/LaunchAgents/com.yourname.bills-due.plist
```

A script that reads your Documents, Desktop or Downloads may make macOS ask for permission the first time it runs.
