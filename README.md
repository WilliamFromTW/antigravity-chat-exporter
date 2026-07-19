# Antigravity Chat Exporter

[English](#english) | [繁體中文](#繁體中文-zh-tw) | [简体中文](#简体中文-zh-cn) | [Tiếng Việt](#tiếng-việt-vi)

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
- Antigravity CLI 1.1.4
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
After installation, the installer writes **Iron Rules** (`.agent/rules/chat_exporter.md`) into your project. These rules instruct the AI to:
1. Immediately trigger the `antigravity-chat-exporter` skill when you ask to export, import, or list backups.
2. Ensure it always passes its own `conversation_id`.
3. Never modify your source code when performing these operations.

Simply tell the Antigravity AI:
- *"Export conversation"* (To export the current chat)
- *"Export all conversations"* (To export all project-related chats)
- *"List backed up conversation IDs"* (To list all available backups)
- *"Import all chats"* (To restore backups to your current workspace)

The AI will automatically trigger the skill and save the logs into `openspec/explorations/explore_log_YYYY-MM-DD.md`.

> 💡 **About Export Naming & Content Scope**
> - **Naming Rule**: Files are named based on the date of the "last message" in the conversation (e.g., `explore_log_2024-05-20.md`).
> - **Content Scope**: The system exports the complete history based on the Conversation ID. Therefore, if a single conversation spans multiple days, the file will include the previous days' chat history as well, without splitting them by date.

To view the logs beautifully, simply double click the generated `chat_history_viewer.html` in your project root!

### Uninstallation
To cleanly remove the skill and its auto-trigger rules, simply run the installer again:
```bash
python install.py
```
Select option `3` to uninstall from the local project, or option `4` to uninstall globally.

### Known Issues
- **`/resume` UI Project Identification**: The Antigravity CLI's `/resume` menu currently cannot dynamically display custom project names for CLI-created sessions. You can only identify which project a conversation belongs to by checking its `conversation_id` inside the backed-up `.antigravity_sync/brains/` directory.

---

## 繁體中文 (zh-TW)

### 簡介
`antigravity-chat-exporter` 是專為 Google Antigravity CLI 開發的強大外掛技能。它能夠直接從系統底層讀取最原始、未經修飾的對話紀錄，並將它們完美排版成帶有本地時間戳記的 Markdown 檔案。這能幫助您永久保留發散思考的過程，並讓您在不同電腦間無縫轉移上下文。

### 核心功能
- **匯出對話與大腦記憶**：將目前的對話紀錄匯出為 Markdown，並完整備份 Antigravity 的底層大腦記憶庫 (`brain/` 與 `.db`) 至 `.antigravity_sync/brains/`，完美支援無縫 Resume。
- **匯入大腦記憶**：一鍵將備份的 Antigravity 大腦記憶還原至本機系統核心，完美支援跨機器復原上下文。
- **Genesis 美型閱讀器**：匯出時全自動生成 `chat_history_viewer.html`。透過三欄式版面，讓您能最方便地同時閱讀 OpenSpec 產出的 SDD 文件（Proposal、Design、Specs 等）與實際對話內容。

### 系統需求
- OpenSpec 1.6.0
- Antigravity CLI 1.1.4
- Python 3.12+
- **完全不需要安裝外部套件**（純原生 Python，僅使用 `os`, `json`, `shutil` 等內建模組）。

### 安裝與移除
我們提供了一鍵式的互動安裝精靈，請在終端機執行：
```bash
python install.py
```
**選單說明：**
1. **單一專案安裝 (Local)**：安裝至指定的專案。*(註：安裝精靈會主動詢問您要安裝的目標資料夾路徑，您可以直接輸入路徑，或按 Enter 預設安裝在當下目錄。)*
2. **全域系統安裝 (Global)**：安裝為全系統通用的 Plugin，日後任何專案皆可使用。
3. **單一專案移除**：移除目前目錄下的安裝與鐵律。
4. **全域系統移除**：移除全系統通用的 Plugin 安裝。

### 使用方式
安裝完成後，安裝精靈會將 **專案鐵律 (Iron Rules)** (`.agent/rules/chat_exporter.md`) 寫入您的專案中。這些鐵律會嚴格限制並指示 AI：
1. 當您要求匯出、匯入或列出備份時，必須立刻觸發 `antigravity-chat-exporter` 技能。
2. 必須永遠主動傳遞它自己的 `conversation_id` 給腳本。
3. 在執行這些操作時，絕對不可修改您的任何專案程式碼。

您只需要像平常一樣對 Antigravity AI 說出：
- *「匯出對話」*（僅匯出當前視窗）
- *「匯出所有對話」*（匯出專案所有的歷史紀錄）
- *「列出備份的對話 ID」*（列出 `.antigravity_sync/brains/` 下的所有備份紀錄）
- *「匯入所有對話」*（將備份還原至當下環境）

AI 就會自動觸發技能，將日誌儲存在 `openspec/explorations/explore_log_YYYY-MM-DD.md`。

> 💡 **關於對話匯出的命名與內容範圍**
> - **檔名規則**：以該對話紀錄中「最後一則訊息」的日期進行命名（如：`explore_log_2024-05-20.md`）。
> - **內容範圍**：系統是以對話 ID (Conversation ID) 為單位進行完整匯出，因此若同一個對話延續了數天，該檔案內將會一併包含前幾天的歷史對話內容，不會依照日期拆檔。

若想以最美的介面回顧對話，只要在專案根目錄點選自動生成的 `chat_history_viewer.html` 即可！

### 移除安裝
若要乾淨移除這項技能與自動寫入的專案鐵律，請再次執行安裝精靈：
```bash
python install.py
```
並在選單中選擇 `3`（移除單一專案安裝）或 `4`（移除全域系統安裝）即可。

### 已知問題
- **`/resume` 介面無法顯示專案名稱**：Antigravity CLI 的 `/resume` 選單目前無法得知是對應哪個專案，您只能從備份的 `.antigravity_sync/brains/` 目錄中的 `conversation_id` 來得知該對話屬於哪個專案了。

---

## 简体中文 (zh-CN)

### 简介
`antigravity-chat-exporter` 是专为 Google Antigravity CLI 开发的强大插件技能。它能够直接从系统底层读取最原始、未经修饰的对话记录，并将它们完美排版成带有本地时间戳的 Markdown 文件。这能帮助您永久保留发散思考的过程，并让您在不同电脑间无缝转移上下文。

### 核心功能
- **导出对话与大脑记忆**：将目前的对话记录导出为 Markdown，并完整备份 Antigravity 的底层大脑记忆库 (`brain/` 与 `.db`) 至 `.antigravity_sync/brains/`，完美支持无缝 Resume。
- **导入大脑记忆**：一键将备份的 Antigravity 大脑记忆还原至本机系统核心，完美支持跨机器复原上下文。
- **Genesis 美型阅读器**：导出时全自动生成 `chat_history_viewer.html`。通过三栏式版面，让您能最方便地同时阅读 OpenSpec 产出的 SDD 文件（Proposal、Design、Specs 等）与实际对话内容。

### 系统要求
- OpenSpec 1.6.0
- Antigravity CLI 1.1.4
- Python 3.12+
- **完全不需要安装外部依赖**（纯原生 Python，仅使用 `os`, `json`, `shutil` 等内置模块）。

### 安装与卸载
我们提供了一键式的交互安装向导，请在终端执行：
```bash
python install.py
```
**菜单说明：**
1. **单项目安装 (Local)**：安装至指定的项目。*(注：安装向导会主动询问您要安装的目标文件夹路径，您可以直接输入路径，或按 Enter 默认安装在当前目录。)*
2. **全局系统安装 (Global)**：安装为全系统通用的 Plugin，日后任何项目皆可使用。
3. **单项目卸载**：移除当前目录下的安装与铁律。
4. **全局系统卸载**：移除全系统通用的 Plugin 安装。

### 使用方式
安装完成后，安装向导会将 **项目铁律 (Iron Rules)** (`.agent/rules/chat_exporter.md`) 写入您的项目中。这些铁律会严格限制并指示 AI：
1. 当您要求导出、导入或列出备份时，必须立刻触发 `antigravity-chat-exporter` 技能。
2. 必须永远主动传递它自己的 `conversation_id` 给脚本。
3. 在执行这些操作时，绝对不可修改您的任何项目代码。

您只需要像平常一样对 Antigravity AI 说出：
- *“导出对话”*（仅导出当前窗口）
- *“导出所有对话”*（导出项目所有的历史记录）
- *“列出备份的对话 ID”*（列出 `.antigravity_sync/brains/` 下的所有备份记录）
- *“导入所有对话”*（将备份还原至当下环境）

AI 就会自动触发技能，将日志储存在 `openspec/explorations/explore_log_YYYY-MM-DD.md`。

> 💡 **关于对话导出的命名与内容范围**
> - **文件名规则**：以该对话记录中“最后一则消息”的日期进行命名（如：`explore_log_2024-05-20.md`）。
> - **内容范围**：系统是以对话 ID (Conversation ID) 为单位进行完整导出，因此若同一个对话延续了数天，该文件内将会一并包含前几天的历史对话内容，不会依照日期拆分。

若想以最美的界面回顾对话，只需在项目根目录双击自动生成的 `chat_history_viewer.html` 即可！

### 卸载说明
若要干净卸载这项技能与自动写入的项目铁律，请再次运行安装向导：
```bash
python install.py
```
并在菜单中选择 `3`（卸载单项目安装）或 `4`（卸载全局系统安装）即可。

### 已知问题
- **`/resume` 界面无法显示项目名称**：Antigravity CLI 的 `/resume` 菜单目前无法得知是对应哪个项目，您只能从备份的 `.antigravity_sync/brains/` 目录中的 `conversation_id` 来得知该对话属于哪个项目了。

---

## Tiếng Việt (VI)

### Tổng quan
`antigravity-chat-exporter` là một kỹ năng tùy chỉnh mạnh mẽ dành cho Google Antigravity CLI. Nó trích xuất các nhật ký trò chuyện nguyên bản từ bộ não bên trong của AI và lưu chúng dưới định dạng Markdown đẹp mắt, hoàn chỉnh với mốc thời gian địa phương. Nó giải quyết một cách hoàn hảo vấn đề mất lịch sử trò chuyện hoặc khi bạn muốn di chuyển ngữ cảnh (context) giữa các máy tính khác nhau.

### Các tính năng cốt lõi
- **Xuất Trò chuyện & Bộ nhớ Não bộ**: Xuất nhật ký trò chuyện hiện tại và sao lưu hoàn toàn bộ nhớ AI Antigravity thô (`brain/` & `.db`) vào `.antigravity_sync/brains/` để phục hồi ngoại tuyến liền mạch.
- **Nhập Bộ nhớ Não bộ**: Khôi phục bộ nhớ AI Antigravity đã sao lưu trở lại lõi hệ thống để tiếp tục ngữ cảnh một cách hoàn hảo trên các máy khác nhau.
- **Genesis HTML Viewer**: Tự động tạo giao diện HTML tuyệt đẹp (`chat_history_viewer.html`) trong quá trình xuất. Giúp việc đọc các tệp SDD của OpenSpec cùng với nội dung trò chuyện thực tế trong bố cục 3 cột trở nên vô cùng thuận tiện.

### Yêu cầu hệ thống
- OpenSpec 1.6.0
- Antigravity CLI 1.1.4
- Python 3.12+
- **Không cần cài đặt thư viện bên ngoài** (chỉ sử dụng các thư viện tiêu chuẩn của Python như `os`, `json`, `shutil`, `datetime`, `argparse`).

### Cài đặt
Chúng tôi cung cấp một trình cài đặt tương tác. Chỉ cần chạy:
```bash
python install.py
```
**Tùy chọn menu:**
1. **Cài đặt cục bộ (Local)**: Cài đặt kỹ năng vào một dự án cụ thể. *(Lưu ý: Trình cài đặt sẽ nhắc bạn nhập đường dẫn thư mục dự án mục tiêu, mặc định là thư mục hiện tại của bạn.)*
2. **Cài đặt toàn cục (Global)**: Cài đặt kỹ năng như một Plugin toàn hệ thống.
3. **Gỡ cài đặt cục bộ**: Xóa kỹ năng khỏi dự án hiện tại.
4. **Gỡ cài đặt toàn cục**: Xóa Plugin toàn hệ thống.

### Cách sử dụng
Sau khi cài đặt, trình cài đặt sẽ ghi các **Quy tắc sắt (Iron Rules)** (`.agent/rules/chat_exporter.md`) vào dự án của bạn. Các quy tắc này hướng dẫn AI:
1. Kích hoạt ngay kỹ năng `antigravity-chat-exporter` khi bạn yêu cầu xuất, nhập hoặc liệt kê các bản sao lưu.
2. Đảm bảo nó luôn truyền `conversation_id` của chính nó.
3. Không bao giờ sửa đổi mã nguồn của bạn khi thực hiện các thao tác này.

Chỉ cần nói với Antigravity AI:
- *"Xuất trò chuyện"* (Để xuất cuộc trò chuyện hiện tại)
- *"Xuất tất cả trò chuyện"* (Để xuất tất cả cuộc trò chuyện liên quan đến dự án)
- *"Liệt kê ID trò chuyện đã sao lưu"* (Để xem danh sách sao lưu)
- *"Nhập tất cả trò chuyện"* (Để khôi phục sao lưu)

AI sẽ tự động kích hoạt kỹ năng và lưu nhật ký vào `openspec/explorations/explore_log_YYYY-MM-DD.md`.

> 💡 **Về Quy tắc Đặt tên & Phạm vi Nội dung Xuất**
> - **Quy tắc đặt tên**: Tệp được đặt tên dựa trên ngày của "tin nhắn cuối cùng" trong cuộc trò chuyện (ví dụ: `explore_log_2024-05-20.md`).
> - **Phạm vi nội dung**: Hệ thống xuất toàn bộ lịch sử dựa trên ID cuộc trò chuyện (Conversation ID). Do đó, nếu một cuộc trò chuyện kéo dài nhiều ngày, tệp sẽ bao gồm cả lịch sử trò chuyện của những ngày trước đó mà không chia tách theo ngày.

Để xem chúng với giao diện đẹp nhất, chỉ cần nhấp đúp vào tệp `chat_history_viewer.html` được tạo tự động trong thư mục dự án của bạn!

### Gỡ cài đặt (Uninstall)
Để xóa sạch kỹ năng và các quy tắc tự động kích hoạt của nó, hãy chạy lại trình cài đặt:
```bash
python install.py
```
Chọn tùy chọn `3` để gỡ cài đặt khỏi dự án cục bộ, hoặc tùy chọn `4` để gỡ cài đặt trên toàn hệ thống.

### Vấn đề đã biết
- **Giao diện `/resume` không hiển thị tên dự án**: Menu `/resume` của Antigravity CLI hiện không thể hiển thị tên dự án cho các phiên trò chuyện được tạo qua CLI. Bạn chỉ có thể xác định cuộc trò chuyện thuộc về dự án nào bằng cách kiểm tra `conversation_id` của nó trong thư mục sao lưu `.antigravity_sync/brains/`.
