# Antigravity Chat Exporter

[English](#english) | [繁體中文](#繁體中文-zh-tw) | [简体中文](#简体中文-zh-cn) | [Tiếng Việt](#tiếng-việt-vi)

---

## English

### Overview
`antigravity-chat-exporter` is a powerful custom skill for the Google Antigravity CLI. It extracts the raw, unedited conversation logs from the AI's internal brain and saves them beautifully formatted in Markdown files, complete with local timestamps. It elegantly solves the issue of losing chat history or wanting to migrate context between different machines.

### Features
- **Export Current Chat**: Exports the ongoing chat session to a daily markdown file.
- **Export All Chats**: Scans the entire brain directory and exports all historical chats related to the current workspace.
- **Smart Formatting**: Automatically converts underlying UTC timestamps to your local time.
- **Auto-Rule Injection**: Installs a rule that automatically triggers the export when you say "export chat".
- **Genesis Chat Viewer**: Auto-deploys `generate_viewer.bat` to your project to turn exported markdown logs into a stunning HTML UI. It supports multi-language UI selection and automatically remembers your custom log directory for future use!

### Requirements
- OpenSpec 1.5.0
- Antigravity CLI 1.1.0
- Python 3.6+
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
After installation, simply tell the Antigravity AI:
- *"Export conversation"* (To export the current chat)
- *"Export all conversations"* (To export all project-related chats)

The AI will automatically trigger the skill and save the logs into `openspec/explorations/explore_log_YYYY-MM-DD.md`.

To view the logs beautifully, double click `generate_viewer.bat` (Windows) or run `sh generate_viewer.sh` (Mac/Linux) in your project root!

### Uninstallation
To cleanly remove the skill and its auto-trigger rules, simply run the installer again:
```bash
python install.py
```
Select option `3` to uninstall from the local project, or option `4` to uninstall globally.

---

## 繁體中文 (zh-TW)

### 簡介
`antigravity-chat-exporter` 是專為 Google Antigravity CLI 開發的強大外掛技能。它能夠直接從系統底層讀取最原始、未經修飾的對話紀錄，並將它們完美排版成帶有本地時間戳記的 Markdown 檔案。這能幫助您永久保留發散思考的過程，並讓您在不同電腦間無縫轉移上下文。

### 核心功能
- **匯出當前對話**：將目前的聊天紀錄獨立匯出為單日 Markdown 檔案。
- **匯出專案所有對話**：全域掃描系統，自動挑出所有跟當前專案有關的歷史紀錄並分日打包。
- **智慧去重機制**：自動將底層的 UTC 時間轉換為本地時間，且多次匯出不會產生重複贅字。
- **專案鐵律注入**：安裝時會自動寫入專案鐵律，讓 AI 聽懂您的匯出指令。
- **Genesis 美型閱讀器**：安裝時會自動部署 `generate_viewer.bat`，一鍵將 Markdown 轉換成絕美的 HTML 閱讀介面。內建四國語言 UI，且若自訂日誌目錄會自動記憶，下次免重複輸入！

### 系統需求
- OpenSpec 1.5.0
- Antigravity CLI 1.1.0
- Python 3.6+
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
安裝完成後，您只需要像平常一樣對 Antigravity AI 說出：
- *「匯出對話」*（僅匯出當前視窗）
- *「匯出所有對話」*（匯出專案所有的歷史紀錄）

AI 就會自動觸發技能，將日誌儲存在 `openspec/explorations/explore_log_YYYY-MM-DD.md`。

若想以最美的介面回顧對話，只要在專案根目錄點兩下 `generate_viewer.bat` (Windows) 或執行 `sh generate_viewer.sh` (Mac/Linux) 即可！

### 移除安裝
若要乾淨移除這項技能與自動寫入的專案鐵律，請再次執行安裝精靈：
```bash
python install.py
```
並在選單中選擇 `3`（移除單一專案安裝）或 `4`（移除全域系統安裝）即可。

---

## 简体中文 (zh-CN)

### 简介
`antigravity-chat-exporter` 是专为 Google Antigravity CLI 开发的强大插件技能。它能够直接从系统底层读取最原始、未经修饰的对话记录，并将它们完美排版成带有本地时间戳的 Markdown 文件。这能帮助您永久保留发散思考的过程，并让您在不同电脑间无缝转移上下文。

### 核心功能
- **导出当前对话**：将目前的聊天记录独立导出为单日 Markdown 文件。
- **导出项目所有对话**：全局扫描系统，自动挑出所有跟当前项目有关的历史记录并按日打包。
- **智能去重机制**：自动将底层的 UTC 时间转换为本地时间，且多次导出不会产生重复内容。
- **项目铁律自动注入**：安装时会自动写入项目铁律，让 AI 听懂您的指令。
- **Genesis 美型阅读器**：安装时会自动部署 `generate_viewer.bat`，一键将 Markdown 转换成绝美的 HTML 阅读界面。内置四国语言 UI，且若自定义日志目录会自动记忆，下次免重复输入！

### 系统要求
- OpenSpec 1.5.0
- Antigravity CLI 1.1.0
- Python 3.6+
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
安装完成后，您只需要像平常一样对 Antigravity AI 说出：
- *“导出对话”*（仅导出当前窗口）
- *“导出所有对话”*（导出项目所有的历史记录）

AI 就会自动触发技能，将日志储存在 `openspec/explorations/explore_log_YYYY-MM-DD.md`。

若想以最美的界面回顾对话，只需在项目根目录双击 `generate_viewer.bat` (Windows) 或执行 `sh generate_viewer.sh` (Mac/Linux) 即可！

### 卸载说明
若要干净卸载这项技能与自动写入的项目铁律，请再次运行安装向导：
```bash
python install.py
```
并在菜单中选择 `3`（卸载单项目安装）或 `4`（卸载全局系统安装）即可。

---

## Tiếng Việt (VI)

### Tổng quan
`antigravity-chat-exporter` là một kỹ năng tùy chỉnh mạnh mẽ dành cho Google Antigravity CLI. Nó trích xuất các nhật ký trò chuyện nguyên bản từ bộ não bên trong của AI và lưu chúng dưới định dạng Markdown đẹp mắt, hoàn chỉnh với mốc thời gian địa phương. Nó giải quyết một cách hoàn hảo vấn đề mất lịch sử trò chuyện hoặc khi bạn muốn di chuyển ngữ cảnh (context) giữa các máy tính khác nhau.

### Các tính năng
- **Xuất trò chuyện hiện tại**: Xuất phiên trò chuyện đang diễn ra thành tệp markdown theo ngày.
- **Xuất tất cả trò chuyện**: Quét toàn bộ thư mục não (brain) và xuất tất cả các cuộc trò chuyện lịch sử liên quan đến không gian làm việc hiện tại.
- **Định dạng thông minh**: Tự động chuyển đổi múi giờ UTC sang giờ địa phương và ngăn chặn nhật ký bị lặp lại một cách thông minh.
- **Tự động thêm quy tắc**: Cài đặt một quy tắc (rule) tự động kích hoạt quá trình xuất khi bạn nói "xuất trò chuyện".
- **Genesis Chat Viewer**: Tự động triển khai `generate_viewer.bat` vào dự án của bạn để biến nhật ký markdown thành giao diện HTML tuyệt đẹp. Hỗ trợ 4 ngôn ngữ giao diện và tự động ghi nhớ thư mục nhật ký tùy chỉnh của bạn cho những lần sử dụng sau!

### Yêu cầu hệ thống
- OpenSpec 1.5.0
- Antigravity CLI 1.1.0
- Python 3.6+
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
Sau khi cài đặt, chỉ cần nói với Antigravity AI:
- *"Xuất trò chuyện"* (Để xuất cuộc trò chuyện hiện tại)
- *"Xuất tất cả trò chuyện"* (Để xuất tất cả cuộc trò chuyện liên quan đến dự án)

AI sẽ tự động kích hoạt kỹ năng và lưu nhật ký vào `openspec/explorations/explore_log_YYYY-MM-DD.md`.

Để xem chúng với giao diện đẹp nhất, hãy nhấp đúp vào `generate_viewer.bat` (Windows) hoặc chạy `sh generate_viewer.sh` (Mac/Linux) trong thư mục dự án của bạn!

### Gỡ cài đặt (Uninstall)
Để xóa sạch kỹ năng và các quy tắc tự động kích hoạt của nó, hãy chạy lại trình cài đặt:
```bash
python install.py
```
Chọn tùy chọn `3` để gỡ cài đặt khỏi dự án cục bộ, hoặc tùy chọn `4` để gỡ cài đặt trên toàn hệ thống.
