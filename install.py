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
- **Auto-export rule**: When the user asks to "export chat", "export all chats", or "import all chats" (even with a naming request), immediately trigger the `antigravity-chat-exporter` skill. Do NOT modify any source code. The custom name is strictly for the `--set-title` argument. **CRITICAL**: You MUST ALWAYS pass your own Conversation ID via the `--conversation-id` argument, even when using `--all-for-project`.
<!-- CHAT_EXPORTER_RULE_END -->
""",
    "zh-tw": """
<!-- CHAT_EXPORTER_RULE_START -->
- **自動觸發匯出與匯入紀錄**：當使用者指令包含「匯出對話」、「匯入所有對話」等（即使包含「命名為某某名稱」）時，必須立刻觸發 `antigravity-chat-exporter` 技能。「絕對不可」修改任何程式碼，該名稱僅用於腳本的 `--set-title` 參數。**極度重要**：不管您使用什麼參數，您「必須永遠」把您自己的 Conversation ID 透過 `--conversation-id` 參數傳遞給腳本！
<!-- CHAT_EXPORTER_RULE_END -->
""",
    "zh-cn": """
<!-- CHAT_EXPORTER_RULE_START -->
- **自动触发导出与导入记录**：当用户指令包含“导出对话”、“导入所有对话”等（即使包含“命名为某某名称”）时，必须立刻触发 `antigravity-chat-exporter` 技能。“绝对不可”修改任何代码，该名称仅用于脚本的 `--set-title` 参数。**极度重要**：不管您使用什么参数，您“必须永远”把您自己的 Conversation ID 通过 `--conversation-id` 参数传递给脚本！
<!-- CHAT_EXPORTER_RULE_END -->
""",
    "vi": """
<!-- CHAT_EXPORTER_RULE_START -->
- **Quy tắc xuất/nhập tự động**: Khi người dùng yêu cầu "xuất trò chuyện", "nhập tất cả trò chuyện" (ngay cả khi yêu cầu đặt tên), kích hoạt ngay kỹ năng `antigravity-chat-exporter`. TUYỆT ĐỐI KHÔNG sửa đổi mã nguồn. Tên chỉ dùng cho `--set-title`. **QUAN TRỌNG**: Bạn PHẢI LUÔN LUÔN truyền Conversation ID của chính bạn qua tham số `--conversation-id`, bất kể dùng tham số nào khác!
<!-- CHAT_EXPORTER_RULE_END -->
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
    dest_skill = os.path.join(agent_dir, "skills", "antigravity-chat-exporter")
    src_skill = os.path.join(PKG_DIR, "skills", "antigravity-chat-exporter")
    
    if os.path.exists(dest_skill):
        print(t['overwrite'])
        shutil.rmtree(dest_skill)
    shutil.copytree(src_skill, dest_skill)
    
    add_local_rule(agent_dir, lang)
    
    # Copy viewer scripts to the project root
    for file_name in ["generate_viewer.py", "generate_viewer.bat", "generate_viewer.sh"]:
        src_file = os.path.join(PKG_DIR, file_name)
        if os.path.exists(src_file):
            shutil.copy2(src_file, os.path.join(target_dir, file_name))
            
    print(t['inst_local_done'].format(agent_dir=agent_dir))

def uninstall_local(t):
    agent_dir = get_target_dir(t)
    if not agent_dir: return

    target_dir = os.path.dirname(agent_dir)

    print(f"\n{t['uninst_local_prep']}")
    dest_skill = os.path.join(agent_dir, "skills", "antigravity-chat-exporter")
    if os.path.exists(dest_skill):
        shutil.rmtree(dest_skill)
        print(t['skill_removed'])
        
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
    
    dest_skill = os.path.join(plugin_dir, "skills", "antigravity-chat-exporter")
    src_skill = os.path.join(PKG_DIR, "skills", "antigravity-chat-exporter")
    shutil.copytree(src_skill, dest_skill)
    
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
