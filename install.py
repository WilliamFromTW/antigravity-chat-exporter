import os
import shutil
import json
import sys
import re

PKG_DIR = os.path.dirname(os.path.abspath(__file__))
GLOBAL_PLUGINS_DIR = os.path.expanduser("~/.gemini/config/plugins")
LOCAL_AGENT_DIR = os.path.join(os.getcwd(), ".agent")

RULE_TEXT = {
    "en": """
<!-- CHAT_EXPORTER_RULE_START -->
- **Auto-export rule**: When the user asks to "export chat", "export all chats", "import all chats", or "list backed up conversation IDs" (even with a naming request), you MUST first automatically execute the Directory Translation Rule (below) to update translations. Then immediately trigger the `antigravity-chat-exporter` skill. Do NOT modify any source code. The custom name is strictly for the `--set-title` argument. **CRITICAL**: You MUST ALWAYS pass your own Conversation ID via the `--conversation-id` argument, even when using `--all-for-project`.
- **List requirement**: When listing backed up conversation IDs to the user, you MUST ALWAYS explicitly include the date/time (Last Modified). Never omit the date when summarizing or presenting the list.
- **Git Commit Rule**: If the user explicitly asks you to `commit` changes related to this project, you MUST write the git commit message in 4 languages (English, Traditional Chinese, Simplified Chinese, and Vietnamese). Format the commit message body with language sections using `[zh-TW]`, `[en]`, `[zh-CN]`, and `[vi]` headers.
- **Directory Translation Rule**: You MUST maintain the file `openspec/changes_i18n.json`. Before exporting logs, or whenever you notice missing directory translations in active changes (`openspec/changes/`), archived changes (`openspec/changes/archive/`), or main specs (`openspec/specs/`), you must proactively translate their directory names into 4 languages (`zh-tw`, `en`, `zh-cn`, `vi`) and update the JSON file. This ensures the HTML viewer generates correctly.
- **Executive Summary Rule**: Before exporting logs, you MUST output a summary of the current session directly in the chat using the exact markdown format: `> [!NOTE]\n> **Executive Summary**\n> <your summary>`. This is required for the HTML viewer to extract and display the summary.
<!-- CHAT_EXPORTER_RULE_END -->

<RULE[openspec-context]>
# OpenSpec Context Recovery Rule
- When the user asks to "read openspec documents", "continue development", or understand a specific feature, you must execute this multidimensional reading strategy:
  1. **Understand Present (What & How)**: Read `openspec/specs/<feature>/spec.md` (or ask the user for the target) to grasp the current strict requirements and scenarios.
  2. **Trace Past (Why)**: Scan `openspec/changes/archive/` for historical changes that modified this feature, and read their `propose.md` or `design.md` to understand the original design rationale.
  3. **Synthesize**: Combine the main specs and archive history to summarize the "Current State" and "Historical Context" for the user, then ask for the next goal. Never confuse historical proposals with current strict specs.
</RULE[openspec-context]>
""",
    "zh-tw": """
<!-- CHAT_EXPORTER_RULE_START -->
- **自動觸發匯出與匯入紀錄**：當使用者指令包含「匯出對話」、「匯入所有對話」或「列出備份的對話 ID」等時，您必須「先自動執行」下方的目錄翻譯鐵律更新 JSON，接著立刻觸發 `antigravity-chat-exporter` 技能。「絕對不可」修改任何程式碼，名稱僅用於 `--set-title` 參數。**極度重要**：不管您使用什麼參數，您「必須永遠」把您自己的 Conversation ID 透過 `--conversation-id` 參數傳遞給腳本！
- **強制列出日期**：當您在向使用者列出備份的對話 ID 時，您「必須永遠」明確地一併列出每個對話的日期與時間 (Last Modified)。在總結或呈現列表時，絕對不允許省略日期。
- **Git Commit 強制規則**：如果使用者明確要求您 `commit` 與此專案相關的變更，您必須強制將 Commit Message 翻譯成四國語言（英文、繁體中文、簡體中文、越南文），並在內容中使用 `[zh-TW]`, `[en]`, `[zh-CN]`, `[vi]` 標題區分。
- **目錄翻譯強制鐵律**：您「必須負責維護」`openspec/changes_i18n.json` 檔案。在每次執行匯出對話前，或是當您發現「活躍的 changes」、「封存的 changes」或「主要 specs」當中有任何目錄名稱尚未記錄於 JSON 中時，您必須主動將其翻譯成四國語言 (`zh-tw`, `en`, `zh-cn`, `vi`) 並更新到該 JSON 檔中。這是為了確保 Viewer 產生 HTML 時能正常顯示翻譯。
- **執行摘要強制鐵律**：在每次執行匯出對話前，您「必須」先在對話中直接輸出一份當前工作階段的總結。格式必須嚴格遵守：`> [!NOTE]\n> **執行摘要**\n> <摘要內容>`。這是為了讓 HTML 閱讀器能夠正確抓取並顯示左側選單的摘要預覽。
<!-- CHAT_EXPORTER_RULE_END -->

<RULE[openspec-context]>
# OpenSpec 快速接續與脈絡還原鐵律 (OpenSpec Context Recovery Rule)
- 當使用者輸入「讀懂openspec文件」、「接續開發」或要求了解特定功能時，您必須執行以下「立體化」讀取策略：
  1. **釐清現狀 (What & How)**：主動讀取 `openspec/specs/<特定功能>/spec.md` (或詢問使用者目標)，掌握當前系統的嚴格需求與情境 (Requirements & Scenarios)。
  2. **追溯過去 (Why)**：接著主動掃描 `openspec/changes/archive/`，尋找曾經修改過該功能的歷史變更，讀取其 `propose.md` 或 `design.md` 以了解設計初衷。
  3. **統整報告**：綜合主 Specs 的規格與 Archive 的歷史背景，向使用者總結「目前功能現況」與「歷史設計脈絡」，並詢問下一步開發目標。切勿將歷史提案與現有規格混淆。
</RULE[openspec-context]>
""",
    "zh-cn": """
<!-- CHAT_EXPORTER_RULE_START -->
- **自动触发导出与导入记录**：当用户指令包含“导出对话”、“导入所有对话”或“列出备份的对话 ID”等时，您必须“先自动执行”下方的目录翻译铁律更新 JSON，接着立刻触发 `antigravity-chat-exporter` 技能。“绝对不可”修改任何代码，名称仅用于 `--set-title` 参数。**极度重要**：不管您使用什么参数，您“必须永远”把您自己的 Conversation ID 通过 `--conversation-id` 参数传递给脚本！
- **强制列出日期**：当您在向用户列出备份的对话 ID 时，您“必须永远”明确地一并列出每个对话的日期与时间 (Last Modified)。在总结或呈现列表时，绝对不允许省略日期。
- **Git Commit 强制规则**：如果用户明确要求您 `commit` 与此项目相关的变更，您必须强制将 Commit Message 翻译成四国语言（英文、繁体中文、简体中文、越南文），并在内容中使用 `[zh-TW]`, `[en]`, `[zh-CN]`, `[vi]` 标题区分。
- **目录翻译强制铁律**：您“必须负责维护”`openspec/changes_i18n.json` 文件。在每次执行导出对话前，或是当您发现“活跃的 changes”、“封存的 changes”或“主要 specs”当中有任何目录名称尚未记录于 JSON 中时，您必须主动将其翻译成四国语言 (`zh-tw`, `en`, `zh-cn`, `vi`) 并更新到该 JSON 档中。这是为了确保 Viewer 产生 HTML 时能正常显示翻译。
- **执行摘要强制铁律**：在每次执行导出对话前，您“必须”先在对话中直接输出一份当前工作阶段的总结。格式必须严格遵守：`> [!NOTE]\n> **执行摘要**\n> <摘要内容>`。这是为了让 HTML 阅读器能够正确抓取并显示左侧菜单的摘要预览。
<!-- CHAT_EXPORTER_RULE_END -->

<RULE[openspec-context]>
# OpenSpec 快速接续与脉络还原铁律 (OpenSpec Context Recovery Rule)
- 当用户输入“读懂openspec文件”、“接续开发”或要求了解特定功能时，您必须执行以下“立体化”读取策略：
  1. **理清现状 (What & How)**：主动读取 `openspec/specs/<特定功能>/spec.md` (或询问用户目标)，掌握当前系统的严格需求与情境 (Requirements & Scenarios)。
  2. **追溯过去 (Why)**：接着主动扫描 `openspec/changes/archive/`，寻找曾经修改过该功能的历史变更，读取其 `propose.md` 或 `design.md` 以了解设计初衷。
  3. **统整报告**：综合主 Specs 的规格与 Archive 的历史背景，向用户总结“目前功能现状”与“历史设计脉络”，并询问下一步开发目标。切勿将历史提案与现有规格混淆。
</RULE[openspec-context]>
""",
    "vi": """
<!-- CHAT_EXPORTER_RULE_START -->
- **Quy tắc xuất/nhập tự động**: Khi người dùng yêu cầu "xuất trò chuyện", "nhập tất cả trò chuyện" hoặc "liệt kê ID trò chuyện đã sao lưu", bạn PHẢI tự động thực thi Quy tắc Dịch Thư mục trước để cập nhật JSON, sau đó kích hoạt ngay kỹ năng `antigravity-chat-exporter`. TUYỆT ĐỐI KHÔNG sửa đổi mã nguồn. Tên chỉ dùng cho `--set-title`. **QUAN TRỌNG**: Bạn PHẢI LUÔN LUÔN truyền Conversation ID của chính bạn qua tham số `--conversation-id`, bất kể dùng tham số nào khác!
- **Bắt buộc hiển thị ngày tháng**: Khi liệt kê các ID trò chuyện đã sao lưu cho người dùng, bạn PHẢI LUÔN LUÔN hiển thị rõ ràng ngày và giờ (Lần sửa đổi cuối). Tuyệt đối không được bỏ qua ngày tháng khi tóm tắt hoặc trình bày danh sách.
- **Quy tắc Git Commit**: Nếu người dùng yêu cầu bạn `commit` các thay đổi liên quan đến dự án này, bạn PHẢI viết thông báo commit bằng 4 ngôn ngữ (Tiếng Anh, Tiếng Trung Phồn thể, Tiếng Trung Giản thể, và Tiếng Việt). Định dạng phần thân của commit với các tiêu đề `[zh-TW]`, `[en]`, `[zh-CN]`, và `[vi]`.
- **Quy tắc Dịch Thư mục**: Bạn PHẢI duy trì tệp `openspec/changes_i18n.json`. Trước khi xuất nhật ký, hoặc bất cứ khi nào bạn thấy các thư mục trong changes đang hoạt động, changes đã lưu trữ, hoặc specs chính chưa có trong tệp JSON, bạn phải chủ động dịch tên thư mục đó sang 4 ngôn ngữ (`zh-tw`, `en`, `zh-cn`, `vi`) và cập nhật vào tệp JSON. Điều này nhằm đảm bảo Trình xem HTML hiển thị bản dịch chính xác.
- **Quy tắc Tóm tắt Thực thi**: Trước khi xuất nhật ký, bạn PHẢI đưa ra tóm tắt về phiên làm việc hiện tại trực tiếp trong cuộc trò chuyện theo đúng định dạng markdown: `> [!NOTE]\n> **Tóm tắt Thực thi**\n> <nội dung tóm tắt>`. Điều này là bắt buộc để trình xem HTML có thể trích xuất và hiển thị tóm tắt ở thanh bên trái.
<!-- CHAT_EXPORTER_RULE_END -->

<RULE[openspec-context]>
# Quy tắc phục hồi bối cảnh OpenSpec (OpenSpec Context Recovery Rule)
- Khi người dùng yêu cầu "đọc tài liệu openspec", "tiếp tục phát triển" hoặc muốn hiểu một tính năng cụ thể, bạn phải thực hiện chiến lược đọc đa chiều sau:
  1. **Hiểu Hiện tại (Cái gì & Như thế nào)**: Đọc `openspec/specs/<tính năng>/spec.md` (hoặc hỏi người dùng mục tiêu) để nắm bắt các yêu cầu và kịch bản nghiêm ngặt hiện tại.
  2. **Truy xuất Quá khứ (Tại sao)**: Quét `openspec/changes/archive/` để tìm các thay đổi lịch sử đã sửa đổi tính năng này và đọc `propose.md` hoặc `design.md` của chúng để hiểu lý do thiết kế ban đầu.
  3. **Tổng hợp**: Kết hợp các thông số kỹ thuật chính và lịch sử lưu trữ để tóm tắt "Trạng thái hiện tại" và "Bối cảnh lịch sử" cho người dùng, sau đó hỏi mục tiêu tiếp theo. Không bao giờ nhầm lẫn các đề xuất lịch sử với các thông số kỹ thuật hiện tại.
</RULE[openspec-context]>
"""
}

I18N = {
    "en": {
        "title": "Antigravity Chat Exporter Setup Wizard",
        "opt1": "Install to current project (Local)",
        "opt2": "Install to system (Global Plugin)",
        "opt3": "Uninstall from current project (Local)",
        "opt4": "Uninstall from system (Global)",
        "opt0": "Exit",
        "prompt": "Please select an action (0-4): ",
        "invalid": "Invalid choice, please enter a number from 0 to 4.",
        "bye": "Goodbye!",
        "prompt_dir": "Enter target project path (leave blank for current directory: {cwd}): ",
        "invalid_dir": "Error: Directory does not exist.",
        "inst_local_prep": "[Preparing Local Installation]",
        "overwrite": ">> Detected older version, overwriting...",
        "inst_local_done": "✅ Installation complete! Skill and rules updated in {agent_dir}",
        "uninst_local_prep": "[Preparing Local Uninstallation]",
        "skill_removed": ">> Skill files removed.",
        "rule_removed": ">> Auto-trigger rule removed.",
        "uninst_local_done": "✅ Local uninstallation complete!",
        "inst_glob_prep": "[Preparing Global Installation]",
        "inst_glob_done": "✅ Global installation complete! Installed at:",
        "restart_msg": "Restart the Antigravity CLI for changes to take effect.",
        "uninst_glob_prep": "[Preparing Global Uninstallation]",
        "uninst_glob_done": "✅ Global plugin removed!",
        "glob_not_found": "⚠️ Global plugin not found."
    },
    "zh-tw": {
        "title": "Antigravity Chat Exporter 安裝精靈",
        "opt1": "安裝到單一專案 (Local)",
        "opt2": "安裝到全域系統 (Global Plugin - 所有專案皆有效)",
        "opt3": "移除單一專案的安裝",
        "opt4": "移除全域系統的安裝",
        "opt0": "離開",
        "prompt": "請選擇要執行的動作 (0-4): ",
        "invalid": "❌ 無效的選擇，請輸入 0-4 的數字。",
        "bye": "再見！",
        "prompt_dir": "請輸入專案路徑 (直接按 Enter 預設為當前目錄: {cwd}): ",
        "invalid_dir": "❌ 錯誤：找不到該目錄。",
        "inst_local_prep": "[準備安裝到單一專案 (Local)]",
        "overwrite": ">> 偵測到舊版技能，正在覆寫...",
        "inst_local_done": "✅ 安裝完成！技能與專案鐵律已更新至 {agent_dir}",
        "uninst_local_prep": "[準備從單一專案移除 (Local)]",
        "skill_removed": ">> 技能檔案已移除。",
        "rule_removed": ">> 專案鐵律已清除。",
        "uninst_local_done": "✅ 移除完成！",
        "inst_glob_prep": "[準備安裝到全域系統 (Global Plugin)]",
        "inst_glob_done": "✅ 全域安裝完成！已安裝至:",
        "restart_msg": "重新啟動 Antigravity CLI 後即可生效。",
        "uninst_glob_prep": "[準備從全域系統移除]",
        "uninst_glob_done": "✅ 全域外掛與鐵律移除完成！",
        "glob_not_found": "⚠️ 找不到已安裝的全域外掛。"
    },
    "zh-cn": {
        "title": "Antigravity Chat Exporter 安装向导",
        "opt1": "安装到单项目 (Local)",
        "opt2": "安装到全局系统 (Global Plugin - 所有项目皆有效)",
        "opt3": "移除单项目的安装",
        "opt4": "移除全局系统的安装",
        "opt0": "离开",
        "prompt": "请选择要执行的动作 (0-4): ",
        "invalid": "❌ 无效的选择，请输入 0-4 的数字。",
        "bye": "再见！",
        "prompt_dir": "请输入项目路径 (直接按 Enter 默认为当前目录: {cwd}): ",
        "invalid_dir": "❌ 错误：找不到该目录。",
        "inst_local_prep": "[准备安装到单项目 (Local)]",
        "overwrite": ">> 检测到旧版技能，正在覆盖...",
        "inst_local_done": "✅ 安装完成！技能与项目铁律已更新至 {agent_dir}",
        "uninst_local_prep": "[准备从单项目移除 (Local)]",
        "skill_removed": ">> 技能文件已移除。",
        "rule_removed": ">> 项目铁律已清除。",
        "uninst_local_done": "✅ 移除完成！",
        "inst_glob_prep": "[准备安装到全局系统 (Global Plugin)]",
        "inst_glob_done": "✅ 全局安装完成！已安装至:",
        "restart_msg": "重新启动 Antigravity CLI 后即可生效。",
        "uninst_glob_prep": "[准备从全局系统移除]",
        "uninst_glob_done": "✅ 全局插件与铁律移除完成！",
        "glob_not_found": "⚠️ 找不到已安装的全局插件。"
    },
    "vi": {
        "title": "Trình hướng dẫn Cài đặt Antigravity Chat Exporter",
        "opt1": "Cài đặt vào dự án cục bộ (Local)",
        "opt2": "Cài đặt vào hệ thống (Global Plugin)",
        "opt3": "Gỡ cài đặt khỏi dự án cục bộ",
        "opt4": "Gỡ cài đặt khỏi hệ thống",
        "opt0": "Thoát",
        "prompt": "Vui lòng chọn một hành động (0-4): ",
        "invalid": "Lựa chọn không hợp lệ, vui lòng nhập số từ 0 đến 4.",
        "bye": "Tạm biệt!",
        "prompt_dir": "Nhập đường dẫn dự án (nhấn Enter để dùng thư mục hiện tại: {cwd}): ",
        "invalid_dir": "❌ Lỗi: Thư mục không tồn tại.",
        "inst_local_prep": "[Chuẩn bị cài đặt cục bộ]",
        "overwrite": ">> Phát hiện phiên bản cũ, đang ghi đè...",
        "inst_local_done": "✅ Cài đặt hoàn tất! Kỹ năng và quy tắc đã được cập nhật trong {agent_dir}",
        "uninst_local_prep": "[Chuẩn bị gỡ cài đặt cục bộ]",
        "skill_removed": ">> Các tệp kỹ năng đã bị xóa.",
        "rule_removed": ">> Quy tắc kích hoạt tự động đã bị xóa.",
        "uninst_local_done": "✅ Gỡ cài đặt cục bộ hoàn tất!",
        "inst_glob_prep": "[Chuẩn bị cài đặt toàn cục]",
        "inst_glob_done": "✅ Cài đặt toàn cục hoàn tất! Đã cài đặt tại:",
        "restart_msg": "Khởi động lại Antigravity CLI để áp dụng các thay đổi.",
        "uninst_glob_prep": "[Chuẩn bị gỡ cài đặt toàn cục]",
        "uninst_glob_done": "✅ Đã xóa plugin toàn cục!",
        "glob_not_found": "⚠️ Không tìm thấy plugin toàn cục."
    }
}

def get_target_dir(t):
    cwd = os.getcwd()
    user_input = input(t["prompt_dir"].format(cwd=cwd)).strip()
    if not user_input:
        target_dir = cwd
    else:
        target_dir = os.path.abspath(user_input)
        
    if not os.path.isdir(target_dir):
        print(t["invalid_dir"])
        return None
        
    return os.path.join(target_dir, ".agent")

def add_local_rule(agent_dir, lang):
    agents_md = os.path.join(agent_dir, "AGENTS.md")
    if not os.path.exists(agent_dir):
        os.makedirs(agent_dir)
    
    content = ""
    if os.path.exists(agents_md):
        with open(agents_md, 'r', encoding='utf-8') as f:
            content = f.read()
            
    if "CHAT_EXPORTER_RULE_START" not in content:
        with open(agents_md, 'a', encoding='utf-8') as f:
            f.write("\n" + RULE_TEXT[lang].strip() + "\n")

def remove_local_rule(agent_dir):
    agents_md = os.path.join(agent_dir, "AGENTS.md")
    if os.path.exists(agents_md):
        with open(agents_md, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = re.sub(r'\n?<!-- CHAT_EXPORTER_RULE_START -->.*?<!-- CHAT_EXPORTER_RULE_END -->\n?', '', content, flags=re.DOTALL)
        
        with open(agents_md, 'w', encoding='utf-8') as f:
            f.write(new_content)

def install_local(t, lang):
    agent_dir = get_target_dir(t)
    if not agent_dir: return

    # target_dir is the parent of agent_dir
    target_dir = os.path.dirname(agent_dir)

    print(f"\n{t['inst_local_prep']}")
    if os.path.exists(os.path.join(agent_dir, "skills", "antigravity-chat-exporter")):
        print(t['overwrite'])
        
    for skill_name in ["antigravity-chat-exporter", "openspec-grill"]:
        dest_skill = os.path.join(agent_dir, "skills", skill_name)
        src_skill = os.path.join(PKG_DIR, "skills", skill_name)
        
        if os.path.exists(dest_skill):
            shutil.rmtree(dest_skill)
        shutil.copytree(src_skill, dest_skill)

    src_wf = os.path.join(PKG_DIR, "workflows")
    if os.path.exists(src_wf):
        dest_wf = os.path.join(agent_dir, "workflows")
        os.makedirs(dest_wf, exist_ok=True)
        for f in os.listdir(src_wf):
            if os.path.isfile(os.path.join(src_wf, f)):
                shutil.copy2(os.path.join(src_wf, f), os.path.join(dest_wf, f))
    
    add_local_rule(agent_dir, lang)
    
    # Note: viewer scripts are no longer copied to the project root
            
    print(t['inst_local_done'].format(agent_dir=agent_dir))

def uninstall_local(t):
    agent_dir = get_target_dir(t)
    if not agent_dir: return

    target_dir = os.path.dirname(agent_dir)

    print(f"\n{t['uninst_local_prep']}")
    for skill_name in ["antigravity-chat-exporter", "openspec-grill"]:
        dest_skill = os.path.join(agent_dir, "skills", skill_name)
        if os.path.exists(dest_skill):
            shutil.rmtree(dest_skill)
    print(t['skill_removed'])

    wf_file = os.path.join(agent_dir, "workflows", "openspec-grill.md")
    if os.path.exists(wf_file):
        os.remove(wf_file)
        
    for file_name in ["generate_viewer.py", "generate_viewer.bat", "generate_viewer.sh", "chat_history_viewer.html"]:
        f_path = os.path.join(target_dir, file_name)
        if os.path.exists(f_path):
            os.remove(f_path)
    
    remove_local_rule(agent_dir)
    print(t['rule_removed'])
    print(t['uninst_local_done'])

def install_global(t, lang):
    print(f"\n{t['inst_glob_prep']}")
    plugin_dir = os.path.join(GLOBAL_PLUGINS_DIR, "antigravity-chat-exporter")
    if os.path.exists(plugin_dir):
        print(t['overwrite'])
        shutil.rmtree(plugin_dir)
        
    os.makedirs(plugin_dir)
    
    for skill_name in ["antigravity-chat-exporter", "openspec-grill"]:
        dest_skill = os.path.join(plugin_dir, "skills", skill_name)
        src_skill = os.path.join(PKG_DIR, "skills", skill_name)
        shutil.copytree(src_skill, dest_skill)

    src_wf = os.path.join(PKG_DIR, "workflows")
    if os.path.exists(src_wf):
        dest_wf = os.path.join(plugin_dir, "workflows")
        os.makedirs(dest_wf, exist_ok=True)
        for f in os.listdir(src_wf):
            if os.path.isfile(os.path.join(src_wf, f)):
                shutil.copy2(os.path.join(src_wf, f), os.path.join(dest_wf, f))
    
    plugin_json = {
        "id": "antigravity-chat-exporter",
        "name": "Antigravity Chat Exporter",
        "description": "Export raw chat logs automatically",
        "version": "1.0.0"
    }
    with open(os.path.join(plugin_dir, "plugin.json"), "w", encoding='utf-8') as f:
        json.dump(plugin_json, f, indent=2)
        
    rules_dir = os.path.join(plugin_dir, "rules")
    os.makedirs(rules_dir)
    with open(os.path.join(rules_dir, "chat_exporter_rule.md"), "w", encoding='utf-8') as f:
        f.write("# Chat Exporter Global Rule\n\n" + RULE_TEXT[lang].strip() + "\n")
        
    print(f"{t['inst_glob_done']} {plugin_dir}")
    print(t['restart_msg'])

def uninstall_global(t):
    print(f"\n{t['uninst_glob_prep']}")
    plugin_dir = os.path.join(GLOBAL_PLUGINS_DIR, "antigravity-chat-exporter")
    if os.path.exists(plugin_dir):
        shutil.rmtree(plugin_dir)
        print(t['uninst_glob_done'])
    else:
        print(t['glob_not_found'])

def main():
    import sys
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    print("="*40)
    print(" Please select language / 請選擇語言")
    print("="*40)
    print(" 1) English")
    print(" 2) 繁體中文 (Traditional Chinese)")
    print(" 3) 简体中文 (Simplified Chinese)")
    print(" 4) Tiếng Việt (Vietnamese)")
    print("="*40)
    
    lang_choice = input("Select / 選擇 (1-4): ").strip()
    
    if lang_choice == '1': lang = "en"
    elif lang_choice == '2': lang = "zh-tw"
    elif lang_choice == '3': lang = "zh-cn"
    elif lang_choice == '4': lang = "vi"
    else:
        print("Invalid choice. Defaulting to English.")
        lang = "en"

    t = I18N[lang]

    while True:
        print("\n" + "="*60)
        print(f" ✨ {t['title']} ✨")
        print("="*60)
        print(f" 1) {t['opt1']}")
        print(f" 2) {t['opt2']}")
        print(f" 3) {t['opt3']}")
        print(f" 4) {t['opt4']}")
        print(f" 0) {t['opt0']}")
        print("="*60)
        
        choice = input(t['prompt']).strip()
        
        if choice == '1':
            install_local(t, lang)
        elif choice == '2':
            install_global(t, lang)
        elif choice == '3':
            uninstall_local(t)
        elif choice == '4':
            uninstall_global(t)
        elif choice == '0':
            print(t['bye'])
            sys.exit(0)
        else:
            print(t['invalid'])

if __name__ == "__main__":
    main()
