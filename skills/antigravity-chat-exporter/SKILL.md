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
```shell
python .agent/skills/antigravity-chat-exporter/scripts/export_log.py --app-data-dir "<App Data Directory>" --conversation-id "1234-5678-abcd" --output-dir "openspec/explorations"
```

### Example Execution (Export ALL Conversations for Project)
If the user asks to export **all** conversations related to the current project, use the `--all-for-project` flag instead of `--conversation-id`:
```shell
python .agent/skills/antigravity-chat-exporter/scripts/export_log.py --app-data-dir "<App Data Directory>" --all-for-project "<Target Project Path>" --output-dir "openspec/explorations"
```

### Example Execution (Set Custom Title)
If the user provides a custom name for the conversation (e.g., "匯出對話並命名為 專案主對話"), you MUST pass the `--set-title` flag and also include the `--conversation-id`. This works alongside any other flags.
```shell
python .agent/skills/antigravity-chat-exporter/scripts/export_log.py --app-data-dir "<App Data Directory>" --conversation-id "1234-5678-abcd" --all-for-project "<Target Project Path>" --output-dir "openspec/explorations" --set-title "專案主對話"
```

### Example Execution (Import ALL Conversations for Project)
If the user asks to "import all chats" or restore the brain state, use the `--import-for-project` flag:
```shell
python .agent/skills/antigravity-chat-exporter/scripts/export_log.py --app-data-dir "<App Data Directory>" --import-for-project "<Target Project Path>"
```

### Example Execution (List Backed Up Conversation IDs)
If the user asks to "list backed up conversation IDs" or similar, use the `--list-backups` flag to print them to your terminal, and then display the results to the user:
```shell
python .agent/skills/antigravity-chat-exporter/scripts/export_log.py --list-backups "<Target Project Path>"
```

3. After running the command, read the output to determine where the file(s) were saved.
4. **Auto-Summarization (Mandatory Step)**
   After ANY export operation (whether "Export conversation", "Export all", or with custom titles), you MUST automatically execute the following summarization workflow for the newly generated or updated markdown file(s):
   - Use the `read_file` or `view_file` tool to read the generated markdown file(s). (If multiple files were generated, process them sequentially).
   - Based on the read context (or your existing memory of the session), generate a concise Executive Summary of the conversation.
   - Use the `replace_file_content` or `multi_replace_file_content` tool to prepend your summary to the VERY TOP of the markdown file(s).
   - Ensure you wrap your summary in a GitHub alert block formatted exactly like this:
     ```markdown
     > [!NOTE]
     > **執行摘要 (Executive Summary)**
     > (Your summary here)
     
     ```
5. Inform the user where the file(s) were saved, and confirm that the Executive Summary was successfully added. Do NOT automatically git commit the logs unless explicitly asked.

