# Antigravity Chat Exporter

[English](#english) | [ç¹é?ä¸­æ?](#ç¹é?ä¸­æ?-zh-tw) | [ç®€ä½“ä¸­?‡](#ç®€ä½“ä¸­??zh-cn) | [Tiáº¿ng Viá»‡t](#tiáº¿ng-viá»‡t-vi)

---

## English

### Overview
`antigravity-chat-exporter` is a powerful custom skill for the Google Antigravity CLI. It extracts the raw, unedited conversation logs from the AI's internal brain and saves them beautifully formatted in Markdown files, complete with local timestamps. It elegantly solves the issue of losing chat history or wanting to migrate context between different machines.

### Core Features
- **Export Chat & Brain Memory**: Exports the current chat session to markdown and perfectly backs up the raw Antigravity AI memory (`brain/` & `.db`) into `.antigravity_sync/brains/` for seamless offline resumption.
- **Import Brain Memory**: Restores the previously backed up Antigravity AI memory back into the system's core to resume context perfectly across machines.
- **Genesis HTML Viewer**: Automatically generates a stunning HTML UI (`chat_history_viewer.html`) during export. This makes it incredibly convenient to read OpenSpec SDD files alongside your actual chat content in a 3-column layout.

### Requirements
- OpenSpec 1.6.0
- Antigravity CLI 1.1.7
- Python 3.12+
- **No external dependencies** (uses only standard libraries like `os`, `json`, `shutil`, `datetime`, `argparse`).

### Installation
We provide an interactive installer. Simply run:
```bash
python install.py
```
**Menu Options:**
1. **Local Install**: Installs the skill to a specific project. *(Note: The installer will prompt you to type the target project directory, defaulting to your current folder.)*
2. **Global Install**: Installs the skill as a system-wide Plugin (`~/.gemini/config/plugins/`).
3. **Local Uninstall**: Removes the skill from the current project.
4. **Global Uninstall**: Removes the system-wide Plugin.

### Usage

Simply tell the Antigravity AI:
- *"Export conversation"* (To export the content of the current chat window)
- *"Export all conversations"* (To export all project-related chats)
- *"List backed up conversation IDs"* (To list all available backups)
- *"Import all chats"* (To restore backups to your current workspace)
- *"Continue development"* (To let the AI automatically read specs and history to seamlessly resume development)

The AI will automatically trigger the skill and save the logs into `openspec/explorations/explore_log_YYYY-MM-DD.md`.

> ?’¡ **About Export Naming & Content Scope**
> - **Naming Rule**: Files are named based on the date of the "last message" in the conversation (e.g., `explore_log_2024-05-20.md`).
> - **Content Scope**: The system exports the complete history based on the Conversation ID. Therefore, if a single conversation spans multiple days, the file will include the previous days' chat history as well, without splitting them by date.

To view the logs beautifully, simply double click the generated `chat_history_viewer.html` in your project root!

### ?? Advanced: Specification-Driven Development (SDD) Workflow
This project now includes the powerful `/openspec-grill` skill. You can use it as part of an advanced OpenSpec workflow:
1. **Explore**: Run `/openspec-explore <idea>` to analyze architecture.
2. **openspec-grill**: Run `/openspec-grill <direction>` to rigorously interrogate the idea against existing specs.
3. **Propose**: Run `/openspec-propose` to convert the interrogated logic into an OpenSpec proposal.
4. **Apply**: Run `/goal /openspec-apply` to auto-implement the code.
*(See [SDD Workflow](.agent/workflows/sdd.md) for the complete guide and flowchart).*

### Uninstallation
To cleanly remove the skill and its auto-trigger rules, simply run the installer again:
```bash
python install.py
```
Select option `3` to uninstall from the local project, or option `4` to uninstall globally.

### Known Issues
- **`/resume` UI Project Identification**: The Antigravity CLI's `/resume` menu currently cannot dynamically display custom project names for CLI-created sessions. You can only identify which project a conversation belongs to by checking its `conversation_id` inside the backed-up `.antigravity_sync/brains/` directory.

---

## ç¹é?ä¸­æ? (zh-TW)

### ç°¡ä?
`antigravity-chat-exporter` ?¯å???Google Antigravity CLI ?‹ç™¼?„å¼·å¤§å??›æ??½ã€‚å??½å??´æ¥å¾ç³»çµ±å?å±¤è??–æ??Ÿå??æœªç¶“ä¿®é£¾ç?å°è©±ç´€?„ï?ä¸¦å?å®ƒå€‘å?ç¾æ??ˆæ?å¸¶æ??¬åœ°?‚é??³è???Markdown æª”æ??‚é€™èƒ½å¹«åŠ©?¨æ°¸ä¹…ä??™ç™¼??€è€ƒç??ç?ï¼Œä¸¦è®“æ‚¨?¨ä??Œé›»?¦é??¡ç¸«è½‰ç§»ä¸Šä??‡ã€?

### ?¸å??Ÿèƒ½
- **?¯å‡ºå°è©±?‡å¤§?¦è???*ï¼šå??®å??„å?è©±ç??„åŒ¯?ºç‚º Markdownï¼Œä¸¦å®Œæ•´?™ä»½ Antigravity ?„å?å±¤å¤§?¦è??¶åº« (`brain/` ??`.db`) ??`.antigravity_sync/brains/`ï¼Œå?ç¾æ”¯?´ç„¡ç¸?Resume??
- **?¯å…¥å¤§è…¦è¨˜æ†¶**ï¼šä??µå??™ä»½??Antigravity å¤§è…¦è¨˜æ†¶?„å??³æœ¬æ©Ÿç³»çµ±æ ¸å¿ƒï?å®Œç??¯æ´è·¨æ??¨å¾©?Ÿä?ä¸‹æ???
- **Genesis ç¾å??±è???*ï¼šåŒ¯?ºæ??¨è‡ª?•ç???`chat_history_viewer.html`?‚é€é?ä¸‰æ?å¼ç??¢ï?è®“æ‚¨?½æ??¹ä¾¿?°å??‚é–±è®€ OpenSpec ?¢å‡º??SDD ?‡ä»¶ï¼ˆProposal?Design?Specs ç­‰ï??‡å¯¦?›å?è©±å…§å®¹ã€?

### ç³»çµ±?€æ±?
- OpenSpec 1.6.0
- Antigravity CLI 1.1.7
- Python 3.12+
- **å®Œå…¨ä¸é?è¦å?è£å??¨å?ä»?*ï¼ˆç??Ÿç? Pythonï¼Œå?ä½¿ç”¨ `os`, `json`, `shutil` ç­‰å…§å»ºæ¨¡çµ„ï???

### å®‰è??‡ç§»??
?‘å€‘æ?ä¾›ä?ä¸€?µå??„ä??•å?è£ç²¾?ˆï?è«‹åœ¨çµ‚ç«¯æ©ŸåŸ·è¡Œï?
```bash
python install.py
```
**?¸å–®èªªæ?ï¼?*
1. **?®ä?å°ˆæ?å®‰è? (Local)**ï¼šå?è£è‡³?‡å??„å?æ¡ˆã€?(è¨»ï?å®‰è?ç²¾é??ƒä¸»?•è©¢?æ‚¨è¦å?è£ç??®æ?è³‡æ?å¤¾è·¯å¾‘ï??¨å¯ä»¥ç›´?¥è¼¸?¥è·¯å¾‘ï??–æ? Enter ?è¨­å®‰è??¨ç•¶ä¸‹ç›®?„ã€?*
2. **?¨å?ç³»çµ±å®‰è? (Global)**ï¼šå?è£ç‚º?¨ç³»çµ±é€šç”¨??Pluginï¼Œæ—¥å¾Œä»»ä½•å?æ¡ˆç??¯ä½¿?¨ã€?
3. **?®ä?å°ˆæ?ç§»é™¤**ï¼šç§»?¤ç›®?ç›®?„ä??„å?è£è??µå???
4. **?¨å?ç³»çµ±ç§»é™¤**ï¼šç§»?¤å…¨ç³»çµ±?šç”¨??Plugin å®‰è???

### ä½¿ç”¨?¹å?

?¨åª?€è¦å?å¹³å¸¸ä¸€æ¨?? Antigravity AI èªªå‡ºï¼?
- *?ŒåŒ¯?ºå?è©±ã€?ï¼ˆåŒ¯?ºç•¶?å?è©±è?çª—å…§å®¹ï?
- *?ŒåŒ¯?ºæ??‰å?è©±ã€?ï¼ˆåŒ¯?ºå?æ¡ˆæ??‰ç?æ­·å²ç´€?„ï?
- *?Œå??ºå?ä»½ç?å°è©± ID??ï¼ˆå???`.antigravity_sync/brains/` ä¸‹ç??€?‰å?ä»½ç??„ï?
- *?ŒåŒ¯?¥æ??‰å?è©±ã€?ï¼ˆå??™ä»½?„å??³ç•¶ä¸‹ç’°å¢ƒï?
- *?Œæ¥çºŒé??¼ã€?ï¼ˆè? AI ?ªå?è®€?–è??¼è?æ­·å²è¨˜æ†¶ï¼Œç„¡ç¸«æ¢å¾©é??¼ç??‹ï?

AI å°±æ??ªå?è§¸ç™¼?€?½ï?å°‡æ—¥èªŒå„²å­˜åœ¨ `openspec/explorations/explore_log_YYYY-MM-DD.md`??

> ?’¡ **?œæ–¼å°è©±?¯å‡º?„å‘½?è??§å®¹ç¯„å?**
> - **æª”å?è¦å?**ï¼šä»¥è©²å?è©±ç??„ä¸­?Œæ?å¾Œä??‡è??¯ã€ç??¥æ??²è??½å?ï¼ˆå?ï¼š`explore_log_2024-05-20.md`ï¼‰ã€?
> - **?§å®¹ç¯„å?**ï¼šç³»çµ±æ˜¯ä»¥å?è©?ID (Conversation ID) ?ºå–®ä½é€²è?å®Œæ•´?¯å‡ºï¼Œå?æ­¤è‹¥?Œä??‹å?è©±å»¶çºŒä??¸å¤©ï¼Œè©²æª”æ??§å??ƒä?ä½µå??«å?å¹¾å¤©?„æ­·?²å?è©±å…§å®¹ï?ä¸æ?ä¾ç…§?¥æ??†æ???

?¥æƒ³ä»¥æ?ç¾ç?ä»‹é¢?é¡§å°è©±ï¼Œåª?€?¨å?æ¡ˆæ ¹?®é??™æ??ªå??¢ç???`chat_history_viewer.html` ?³å¯ï¼?

### ?? ?²é??Ÿèƒ½ï¼šè??¼é??•é???(SDD) å·¥ä?æµ?
?¬å?æ¡ˆç¾å·²å…§å»ºè?å¼·ç? `/openspec-grill` ?·å??€?½ï??¨å¯ä»¥æ­??OpenSpec ?²è??²é??‹ç™¼ï¼?
1. **?¢å? (Explore)**ï¼šä½¿??`/openspec-explore <?°é?æ±?` ?†æ??€è¡“æ¶æ§‹ã€?
2. **?¡æ??·å? (openspec-grill)**ï¼šä½¿??`/openspec-grill <?¹å?>` è®?AI ?¿ç¾?‰è??¼åš´?¼æª¢è¦–æ‚¨?„é?å­ã€?
3. **?æ? (Propose)**ï¼šç¢ºèªç„¡èª¤å?ï¼Œè¼¸??`/openspec-propose` å°‡å…±è­˜è??–ç‚ºæ¨™æ??æ???
4. **?·è? (Apply)**ï¼šé€é? `/goal /openspec-apply` è®?AI ?¨è‡ª?•é??¼è?æ¸¬è©¦??
*(è©³ç´°æµç??–è??ä?ç§˜è¨£è«‹è? [SDD çµ‚æ¥µå·¥ä?æµ](.agent/workflows/sdd.md))*??

### ç§»é™¤å®‰è?
?¥è?ä¹¾æ·¨ç§»é™¤?™é??€?½è??ªå?å¯«å…¥?„å?æ¡ˆéµå¾‹ï?è«‹å?æ¬¡åŸ·è¡Œå?è£ç²¾?ˆï?
```bash
python install.py
```
ä¸¦åœ¨?¸å–®ä¸­é¸??`3`ï¼ˆç§»?¤å–®ä¸€å°ˆæ?å®‰è?ï¼‰æ? `4`ï¼ˆç§»?¤å…¨?Ÿç³»çµ±å?è£ï??³å¯??

### å·²çŸ¥?é?
- **`/resume` ä»‹é¢?¡æ?é¡¯ç¤ºå°ˆæ??ç¨±**ï¼šAntigravity CLI ??`/resume` ?¸å–®?®å??¡æ?å¾—çŸ¥?¯å??‰å“ª?‹å?æ¡ˆï??¨åª?½å??™ä»½??`.antigravity_sync/brains/` ?®é?ä¸­ç? `conversation_id` ä¾†å??¥è©²å°è©±å±¬æ–¼?ªå€‹å?æ¡ˆä???

---

## ç®€ä½“ä¸­??(zh-CN)

### ç®€ä»?
`antigravity-chat-exporter` ?¯ä?ä¸?Google Antigravity CLI å¼€?‘ç?å¼ºå¤§?’ä»¶?€?½ã€‚å??½å??´æ¥ä»ç³»ç»Ÿå?å±‚è¯»?–æ??Ÿå??æœªç»ä¿®é¥°ç?å¯¹è?è®°å?ï¼Œå¹¶å°†å?ä»¬å?ç¾æ??ˆæ?å¸¦æ??¬åœ°?¶é—´?³ç? Markdown ?‡ä»¶?‚è??½å¸®?©æ‚¨æ°¸ä?ä¿ç??‘æ•£?è€ƒç?è¿‡ç?ï¼Œå¹¶è®©æ‚¨?¨ä??Œç”µ?‘é—´? ç?è½¬ç§»ä¸Šä??‡ã€?

### ?¸å??Ÿèƒ½
- **å¯¼å‡ºå¯¹è?ä¸å¤§?‘è®°å¿?*ï¼šå??®å??„å¯¹è¯è®°å½•å¯¼?ºä¸º Markdownï¼Œå¹¶å®Œæ•´å¤‡ä»½ Antigravity ?„å?å±‚å¤§?‘è®°å¿†å? (`brain/` ä¸?`.db`) ??`.antigravity_sync/brains/`ï¼Œå?ç¾æ”¯?æ?ç¼?Resume??
- **å¯¼å…¥å¤§è?è®°å?**ï¼šä??®å?å¤‡ä»½??Antigravity å¤§è?è®°å?è¿˜å??³æœ¬?ºç³»ç»Ÿæ ¸å¿ƒï?å®Œç??¯æ?è·¨æœº?¨å??Ÿä?ä¸‹æ???
- **Genesis ç¾å??…è¯»??*ï¼šå¯¼?ºæ—¶?¨è‡ª?¨ç???`chat_history_viewer.html`?‚é€šè?ä¸‰æ?å¼ç??¢ï?è®©æ‚¨?½æ??¹ä¾¿?°å??¶é?è¯?OpenSpec äº§å‡º??SDD ?‡ä»¶ï¼ˆProposal?Design?Specs ç­‰ï?ä¸å??…å¯¹è¯å?å®¹ã€?

### ç³»ç?è¦æ?
- OpenSpec 1.6.0
- Antigravity CLI 1.1.7
- Python 3.12+
- **å®Œå…¨ä¸é?è¦å?è£…å??¨ä?èµ?*ï¼ˆçº¯?Ÿç? Pythonï¼Œä?ä½¿ç”¨ `os`, `json`, `shutil` ç­‰å?ç½®æ¨¡?—ï???

### å®‰è?ä¸å¸è½?
?‘ä»¬?ä?äº†ä??®å??„äº¤äº’å?è£…å?å¯¼ï?è¯·åœ¨ç»ˆç«¯?§è?ï¼?
```bash
python install.py
```
**?œå?è¯´æ?ï¼?*
1. **?•é¡¹?®å?è£?(Local)**ï¼šå?è£…è‡³?‡å??„é¡¹?®ã€?(æ³¨ï?å®‰è??‘å¯¼ä¼šä¸»?¨è¯¢?®æ‚¨è¦å?è£…ç??®æ??‡ä»¶å¤¹è·¯å¾„ï??¨å¯ä»¥ç›´?¥è??¥è·¯å¾„ï??–æ? Enter é»˜è®¤å®‰è??¨å??ç›®å½•ã€?*
2. **?¨å?ç³»ç?å®‰è? (Global)**ï¼šå?è£…ä¸º?¨ç³»ç»Ÿé€šç”¨??Pluginï¼Œæ—¥?ä»»ä½•é¡¹?®ç??¯ä½¿?¨ã€?
3. **?•é¡¹?®å¸è½?*ï¼šç§»?¤å??ç›®å½•ä??„å?è£…ä??å???
4. **?¨å?ç³»ç??¸è½½**ï¼šç§»?¤å…¨ç³»ç??šç”¨??Plugin å®‰è???

### ä½¿ç”¨?¹å?

?¨åª?€è¦å?å¹³å¸¸ä¸€?·å¯¹ Antigravity AI è¯´å‡ºï¼?
- *?œå¯¼?ºå¯¹è¯â€?ï¼ˆå¯¼?ºå??å¯¹è¯ç????å®¹ï?
- *?œå¯¼?ºæ??‰å¯¹è¯â€?ï¼ˆå¯¼?ºé¡¹?®æ??‰ç??†å²è®°å?ï¼?
- *?œå??ºå?ä»½ç?å¯¹è? ID??ï¼ˆå???`.antigravity_sync/brains/` ä¸‹ç??€?‰å?ä»½è®°å½•ï?
- *?œå¯¼?¥æ??‰å¯¹è¯â€?ï¼ˆå?å¤‡ä»½è¿˜å??³å?ä¸‹ç¯å¢ƒï?
- *?œæ¥ç»­å??‘â€?ï¼ˆè®© AI ?ªåŠ¨è¯»å?è§„æ ¼ä¸å??²è®°å¿†ï?? ç??¢å?å¼€?‘çŠ¶?ï?

AI å°±ä??ªåŠ¨è§¦å??€?½ï?å°†æ—¥å¿—å‚¨å­˜åœ¨ `openspec/explorations/explore_log_YYYY-MM-DD.md`??

> ?’¡ **?³ä?å¯¹è?å¯¼å‡º?„å‘½?ä??…å®¹?ƒå›´**
> - **?‡ä»¶?è???*ï¼šä»¥è¯¥å¯¹è¯è®°å½•ä¸­?œæ??ä??™æ??¯â€ç??¥æ?è¿›è??½å?ï¼ˆå?ï¼š`explore_log_2024-05-20.md`ï¼‰ã€?
> - **?…å®¹?ƒå›´**ï¼šç³»ç»Ÿæ˜¯ä»¥å¯¹è¯?ID (Conversation ID) ä¸ºå?ä½è?è¡Œå??´å¯¼?ºï?? æ­¤?¥å?ä¸€ä¸ªå¯¹è¯å»¶ç»­ä??°å¤©ï¼Œè¯¥?‡ä»¶?…å?ä¼šä?å¹¶å??«å?? å¤©?„å??²å¯¹è¯å?å®¹ï?ä¸ä?ä¾ç…§?¥æ??†å???

?¥æƒ³ä»¥æ?ç¾ç??Œé¢?é¡¾å¯¹è?ï¼Œåª?€?¨é¡¹?®æ ¹?®å??Œå‡»?ªåŠ¨?Ÿæ???`chat_history_viewer.html` ?³å¯ï¼?

### ?? è¿›é˜¶?Ÿèƒ½ï¼šè??¼é©±?¨å???(SDD) å·¥ä?æµ?
?¬é¡¹?®ç°å·²å?ç½®è?å¼ºç? `/openspec-grill` ?·é—®?€?½ï??¨å¯ä»¥æ­??OpenSpec è¿›è?è¿›é˜¶å¼€?‘ï?
1. **?¢å? (Explore)**ï¼šä½¿??`/openspec-explore <?°é?æ±?` ?†æ??€?¯æ¶?„ã€?
2. **? æ??·é—® (openspec-grill)**ï¼šä½¿??`/openspec-grill <?¹å?>` è®?AI ?¿ç°?‰è??¼ä¸¥?¼æ?è§†æ‚¨?„ç‚¹å­ã€?
3. **?æ? (Propose)**ï¼šç¡®è®¤æ?è¯¯å?ï¼Œè???`/openspec-propose` å°†å…±è¯†è½¬?–ä¸º?‡å??æ???
4. **?§è? (Apply)**ï¼šé€è? `/goal /openspec-apply` è®?AI ?¨è‡ª?¨å??‘ä?æµ‹è???
*(è¯¦ç?æµç??¾ä??ä?ç§˜è?è¯·è? [SDD ç»ˆæ?å·¥ä?æµ](.agent/workflows/sdd.md))*??

### ?¸è½½è¯´æ?
?¥è?å¹²å??¸è½½è¿™é¡¹?€?½ä??ªåŠ¨?™å…¥?„é¡¹?®é?å¾‹ï?è¯·å?æ¬¡è?è¡Œå?è£…å?å¯¼ï?
```bash
python install.py
```
å¹¶åœ¨?œå?ä¸­é€‰æ‹© `3`ï¼ˆå¸è½½å?é¡¹ç›®å®‰è?ï¼‰æ? `4`ï¼ˆå¸è½½å…¨å±€ç³»ç?å®‰è?ï¼‰å³?¯ã€?

### å·²çŸ¥?®é?
- **`/resume` ?Œé¢? æ??¾ç¤ºé¡¹ç›®?ç§°**ï¼šAntigravity CLI ??`/resume` ?œå??®å?? æ?å¾—çŸ¥?¯å¯¹åº”å“ªä¸ªé¡¹?®ï??¨åª?½ä?å¤‡ä»½??`.antigravity_sync/brains/` ?®å?ä¸­ç? `conversation_id` ?¥å??¥è¯¥å¯¹è?å±ä??ªä¸ªé¡¹ç›®äº†ã€?

---

## Tiáº¿ng Viá»‡t (VI)

### Tá»•ng quan
`antigravity-chat-exporter` l? má»™t ká»?n?ng tÃ¹y chá»‰nh máº¡nh máº?d?nh cho Google Antigravity CLI. NÃ³ trÃ­ch xuáº¥t cÃ¡c nháº­t kÃ½ trÃ² chuyá»‡n nguyÃªn báº£n tá»?bá»?nÃ£o bÃªn trong cá»§a AI v? lÆ°u chÃºng dÆ°á»›i ?á»‹nh dáº¡ng Markdown ?áº¹p máº¯t, ho?n chá»‰nh vá»›i má»‘c thá»i gian ?á»‹a phÆ°Æ¡ng. NÃ³ giáº£i quyáº¿t má»™t cÃ¡ch ho?n háº£o váº¥n ?á»?máº¥t lá»‹ch sá»?trÃ² chuyá»‡n hoáº·c khi báº¡n muá»‘n di chuyá»ƒn ngá»?cáº£nh (context) giá»¯a cÃ¡c mÃ¡y tÃ­nh khÃ¡c nhau.

### CÃ¡c tÃ­nh n?ng cá»‘t lÃµi
- **Xuáº¥t TrÃ² chuyá»‡n & Bá»?nhá»?NÃ£o bá»?*: Xuáº¥t nháº­t kÃ½ trÃ² chuyá»‡n hiá»‡n táº¡i v? sao lÆ°u ho?n to?n bá»?nhá»?AI Antigravity thÃ´ (`brain/` & `.db`) v?o `.antigravity_sync/brains/` ?á»?phá»¥c há»“i ngoáº¡i tuyáº¿n liá»n máº¡ch.
- **Nháº­p Bá»?nhá»?NÃ£o bá»?*: KhÃ´i phá»¥c bá»?nhá»?AI Antigravity ?Ã£ sao lÆ°u trá»?láº¡i lÃµi há»?thá»‘ng ?á»?tiáº¿p tá»¥c ngá»?cáº£nh má»™t cÃ¡ch ho?n háº£o trÃªn cÃ¡c mÃ¡y khÃ¡c nhau.
- **Genesis HTML Viewer**: Tá»??á»™ng táº¡o giao diá»‡n HTML tuyá»‡t ?áº¹p (`chat_history_viewer.html`) trong quÃ¡ trÃ¬nh xuáº¥t. GiÃºp viá»‡c ?á»c cÃ¡c tá»‡p SDD cá»§a OpenSpec cÃ¹ng vá»›i ná»™i dung trÃ² chuyá»‡n thá»±c táº?trong bá»?cá»¥c 3 cá»™t trá»?nÃªn vÃ´ cÃ¹ng thuáº­n tiá»‡n.

### YÃªu cáº§u há»?thá»‘ng
- OpenSpec 1.6.0
- Antigravity CLI 1.1.7
- Python 3.12+
- **KhÃ´ng cáº§n c?i ?áº·t thÆ° viá»‡n bÃªn ngo?i** (chá»?sá»?dá»¥ng cÃ¡c thÆ° viá»‡n tiÃªu chuáº©n cá»§a Python nhÆ° `os`, `json`, `shutil`, `datetime`, `argparse`).

### C?i ?áº·t
ChÃºng tÃ´i cung cáº¥p má»™t trÃ¬nh c?i ?áº·t tÆ°Æ¡ng tÃ¡c. Chá»?cáº§n cháº¡y:
```bash
python install.py
```
**TÃ¹y chá»n menu:**
1. **C?i ?áº·t cá»¥c bá»?(Local)**: C?i ?áº·t ká»?n?ng v?o má»™t dá»?Ã¡n cá»?thá»? *(LÆ°u Ã½: TrÃ¬nh c?i ?áº·t sáº?nháº¯c báº¡n nháº­p ?Æ°á»ng dáº«n thÆ° má»¥c dá»?Ã¡n má»¥c tiÃªu, máº·c ?á»‹nh l? thÆ° má»¥c hiá»‡n táº¡i cá»§a báº¡n.)*
2. **C?i ?áº·t to?n cá»¥c (Global)**: C?i ?áº·t ká»?n?ng nhÆ° má»™t Plugin to?n há»?thá»‘ng.
3. **Gá»?c?i ?áº·t cá»¥c bá»?*: XÃ³a ká»?n?ng khá»i dá»?Ã¡n hiá»‡n táº¡i.
4. **Gá»?c?i ?áº·t to?n cá»¥c**: XÃ³a Plugin to?n há»?thá»‘ng.

### CÃ¡ch sá»?dá»¥ng

Chá»?cáº§n nÃ³i vá»›i Antigravity AI:
- *"Xuáº¥t trÃ² chuyá»‡n"* (?á»?xuáº¥t ná»™i dung cá»§a cá»­a sá»?trÃ² chuyá»‡n hiá»‡n táº¡i)
- *"Xuáº¥t táº¥t cáº?trÃ² chuyá»‡n"* (?á»?xuáº¥t táº¥t cáº?cuá»™c trÃ² chuyá»‡n liÃªn quan ?áº¿n dá»?Ã¡n)
- *"Liá»‡t kÃª ID trÃ² chuyá»‡n ?Ã£ sao lÆ°u"* (?á»?xem danh sÃ¡ch sao lÆ°u)
- *"Nháº­p táº¥t cáº?trÃ² chuyá»‡n"* (?á»?khÃ´i phá»¥c sao lÆ°u)
- *"Tiáº¿p tá»¥c phÃ¡t triá»ƒn"* (?á»?AI tá»??á»™ng ?á»c thÃ´ng sá»?ká»?thuáº­t v? lá»‹ch sá»? giÃºp khÃ´i phá»¥c tráº¡ng thÃ¡i phÃ¡t triá»ƒn liá»n máº¡ch)

AI sáº?tá»??á»™ng kÃ­ch hoáº¡t ká»?n?ng v? lÆ°u nháº­t kÃ½ v?o `openspec/explorations/explore_log_YYYY-MM-DD.md`.

> ?’¡ **Vá»?Quy táº¯c ?áº·t tÃªn & Pháº¡m vi Ná»™i dung Xuáº¥t**
> - **Quy táº¯c ?áº·t tÃªn**: Tá»‡p ?Æ°á»£c ?áº·t tÃªn dá»±a trÃªn ng?y cá»§a "tin nháº¯n cuá»‘i cÃ¹ng" trong cuá»™c trÃ² chuyá»‡n (vÃ­ dá»? `explore_log_2024-05-20.md`).
> - **Pháº¡m vi ná»™i dung**: Há»?thá»‘ng xuáº¥t to?n bá»?lá»‹ch sá»?dá»±a trÃªn ID cuá»™c trÃ² chuyá»‡n (Conversation ID). Do ?Ã³, náº¿u má»™t cuá»™c trÃ² chuyá»‡n kÃ©o d?i nhiá»u ng?y, tá»‡p sáº?bao gá»“m cáº?lá»‹ch sá»?trÃ² chuyá»‡n cá»§a nhá»¯ng ng?y trÆ°á»›c ?Ã³ m? khÃ´ng chia tÃ¡ch theo ng?y.

?á»?xem nháº­t kÃ½ má»™t cÃ¡ch ?áº¹p máº¯t, chá»?cáº§n nháº¥p ?Ãºp v?o tá»‡p `chat_history_viewer.html` ?Æ°á»£c táº¡o tá»??á»™ng trong thÆ° má»¥c gá»‘c cá»§a dá»?Ã¡n!

### ?? NÃ¢ng cao: Quy trÃ¬nh PhÃ¡t triá»ƒn Theo ThÃ´ng sá»?Ká»?thuáº­t (SDD)
Dá»?Ã¡n n?y hiá»‡n ?Ã£ tÃ­ch há»£p ká»?n?ng `/openspec-grill` máº¡nh máº? Báº¡n cÃ³ thá»?sá»?dá»¥ng nÃ³ nhÆ° má»™t pháº§n cá»§a quy trÃ¬nh OpenSpec nÃ¢ng cao:
1. **KhÃ¡m phÃ¡ (Explore)**: Cháº¡y `/openspec-explore <Ã½ tÆ°á»Ÿng>` ?á»?phÃ¢n tÃ­ch kiáº¿n trÃºc.
2. **Tháº©m váº¥n (openspec-grill)**: Cháº¡y `/openspec-grill <hÆ°á»›ng ?i>` ?á»?cháº¥t váº¥n nghiÃªm ngáº·t Ã½ tÆ°á»Ÿng so vá»›i thÃ´ng sá»?ká»?thuáº­t hiá»‡n táº¡i.
3. **?á»?xuáº¥t (Propose)**: Cháº¡y `/openspec-propose` ?á»?chuyá»ƒn ?á»•i logic ?Ã£ thá»‘ng nháº¥t th?nh ?á»?xuáº¥t OpenSpec.
4. **?p dá»¥ng (Apply)**: Cháº¡y `/goal /openspec-apply` ?á»?tá»??á»™ng triá»ƒn khai mÃ£.
*(Xem [Quy trÃ¬nh SDD](.agent/workflows/sdd.md) ?á»?biáº¿t hÆ°á»›ng dáº«n chi tiáº¿t v? sÆ¡ ?á»?.*

### Gá»?c?i ?áº·t (Uninstall)
?á»?xÃ³a sáº¡ch ká»?n?ng v? cÃ¡c quy táº¯c tá»??á»™ng kÃ­ch hoáº¡t cá»§a nÃ³, hÃ£y cháº¡y láº¡i trÃ¬nh c?i ?áº·t:
```bash
python install.py
```
Chá»n tÃ¹y chá»n `3` ?á»?gá»?c?i ?áº·t khá»i dá»?Ã¡n cá»¥c bá»? hoáº·c tÃ¹y chá»n `4` ?á»?gá»?c?i ?áº·t trÃªn to?n há»?thá»‘ng.

### Váº¥n ?á»??Ã£ biáº¿t
- **Giao diá»‡n `/resume` khÃ´ng hiá»ƒn thá»?tÃªn dá»?Ã¡n**: Menu `/resume` cá»§a Antigravity CLI hiá»‡n khÃ´ng thá»?hiá»ƒn thá»?tÃªn dá»?Ã¡n cho cÃ¡c phiÃªn trÃ² chuyá»‡n ?Æ°á»£c táº¡o qua CLI. Báº¡n chá»?cÃ³ thá»?xÃ¡c ?á»‹nh cuá»™c trÃ² chuyá»‡n thuá»™c vá»?dá»?Ã¡n n?o báº±ng cÃ¡ch kiá»ƒm tra `conversation_id` cá»§a nÃ³ trong thÆ° má»¥c sao lÆ°u `.antigravity_sync/brains/`.
