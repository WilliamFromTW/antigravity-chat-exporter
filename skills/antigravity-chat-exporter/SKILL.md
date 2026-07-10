---
name: antigravity-chat-exporter
description: Export the entire raw, unedited conversation log to a markdown file.
---

# Export Raw Conversation Log

When the user asks to "export the conversation", "dump the log", or use the `antigravity-chat-exporter` skill, you must execute the provided python script to extract the conversation transcript and save it to the workspace.

## Usage Instructions

1. Use the `run_command` tool to execute the python script located at `scripts/export_log.py` within this skill directory.
2. The script requires three arguments:
   - `--app-data-dir`: The path to the Antigravity App Data Directory.
   - `--conversation-id`: The current Conversation ID.
   - `--output-dir`: The directory where the log should be saved (e.g., `openspec/explorations`).

**How to find the variables:**
You can find the `App Data Directory` and `Conversation ID` within your system prompt instructions (usually under the `<user_information>` section or `<artifacts>` section).

### Example Execution (Export Current Conversation)
```powershell
python .agent/skills/antigravity-chat-exporter/scripts/export_log.py --app-data-dir "C:\Users\username\.gemini\antigravity-cli" --conversation-id "1234-5678-abcd" --output-dir "openspec/explorations"
```

### Example Execution (Export ALL Conversations for Project)
If the user asks to export **all** conversations related to the current project, use the `--all-for-project` flag instead of `--conversation-id`:
```powershell
python .agent/skills/antigravity-chat-exporter/scripts/export_log.py --app-data-dir "C:\Users\username\.gemini\antigravity-cli" --all-for-project "C:\Users\username\syncmyantigravityproject" --output-dir "openspec/explorations"
```

3. After running the command, inform the user where the file(s) were saved. Do NOT automatically git commit the logs unless explicitly asked.
