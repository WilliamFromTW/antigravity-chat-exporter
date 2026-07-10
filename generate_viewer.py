import os
import glob
import json
import webbrowser

I18N = {
    "en": {
        "title": "Exploration Logs",
        "subtitle": "Antigravity Chat Exporter",
        "no_logs": "No logs found.",
        "html_title": "Genesis Chat Log Viewer"
    },
    "zh-tw": {
        "title": "對話探索日誌",
        "subtitle": "Antigravity 對話匯出器",
        "no_logs": "找不到任何日誌檔案。",
        "html_title": "Genesis 對話閱讀器"
    },
    "zh-cn": {
        "title": "对话探索日志",
        "subtitle": "Antigravity 对话导出器",
        "no_logs": "找不到任何日志文件。",
        "html_title": "Genesis 对话阅读器"
    },
    "vi": {
        "title": "Nhật ký Khám phá",
        "subtitle": "Trình xuất trò chuyện Antigravity",
        "no_logs": "Không tìm thấy nhật ký.",
        "html_title": "Trình xem nhật ký Genesis"
    }
}

def choose_language():
    print("="*40)
    print(" Please select UI language / 請選擇介面語言")
    print("="*40)
    print(" 1) English")
    print(" 2) 繁體中文 (Traditional Chinese)")
    print(" 3) 简体中文 (Simplified Chinese)")
    print(" 4) Tiếng Việt (Vietnamese)")
    print("="*40)
    
    choice = input("Select / 選擇 (1-4): ").strip()
    if choice == '1': return "en"
    elif choice == '2': return "zh-tw"
    elif choice == '3': return "zh-cn"
    elif choice == '4': return "vi"
    else: return "en"

def generate_viewer():
    lang = choose_language()
    t = I18N[lang]
    
    log_dir = "openspec/explorations"
    output_file = "chat_history_viewer.html"
    
    if not os.path.exists(log_dir):
        print(f"Error: Directory '{log_dir}' not found.")
        return

    md_files = glob.glob(os.path.join(log_dir, "explore_log_*.md"))
    if not md_files:
        print(f"No markdown logs found in {log_dir}")
        return

    logs = {}
    for f in md_files:
        filename = os.path.basename(f)
        date_str = filename.replace('explore_log_', '').replace('.md', '')
        with open(f, 'r', encoding='utf-8') as file:
            logs[date_str] = file.read()
            
    # Sort dates descending (newest first)
    dates = sorted(logs.keys(), reverse=True)
    # Safely escape HTML closing tags so they don't break the <script> block
    logs_json = json.dumps(logs).replace("</", "<\\/")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t['html_title']}</title>
    <!-- Genesis Typography -->
    <link href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <!-- Marked.js for Markdown parsing -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    
    <style>
        :root {{
            --primary: #6366F1;
            --primary-hover: #4F46E5;
            --neutral: #9C9C9C;
            --bg: #FAFAFA;
            --surface: #FFFFFF;
            --text-primary: #0A0A0A;
            --text-secondary: #6B6B6B;
            --border: #E8E8EC;
            --font-display: 'General Sans', sans-serif;
            --font-body: 'DM Sans', sans-serif;
            --font-code: 'JetBrains Mono', monospace;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 0;
            background-color: var(--bg);
            color: var(--text-primary);
            font-family: var(--font-body);
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--font-display);
            font-weight: 700;
            letter-spacing: -0.03em;
            color: var(--text-primary);
        }}

        .sidebar {{
            width: 320px;
            background: var(--surface);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            padding: 32px 24px;
            overflow-y: auto;
            z-index: 10;
            box-shadow: 2px 0 12px rgba(0,0,0,0.02);
        }}

        .brand-header {{
            margin-bottom: 40px;
        }}

        .brand-header h1 {{
            font-size: 24px;
            margin: 0;
        }}
        
        .brand-header p {{
            color: var(--text-secondary);
            font-size: 13px;
            margin: 4px 0 0 0;
        }}

        .date-btn {{
            background: transparent;
            border: 1px solid transparent;
            text-align: left;
            padding: 12px 16px;
            border-radius: 6px;
            font-family: var(--font-body);
            font-size: 15px;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            margin-bottom: 8px;
            transition: all 0.2s;
            display: flex;
            align-items: center;
        }}

        .date-btn::before {{
            content: "📄";
            margin-right: 12px;
            font-size: 14px;
            opacity: 0.5;
        }}

        .date-btn:hover {{
            background: var(--bg);
            color: var(--text-primary);
            border-color: var(--border);
        }}

        .date-btn:focus-visible {{
            outline: none;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.12);
            border-color: var(--primary);
        }}

        .date-btn.active {{
            background: var(--primary);
            color: var(--surface);
            box-shadow: 0 4px 12px rgba(99,102,241,0.35);
            transform: translateY(-1px);
        }}

        .date-btn.active::before {{
            opacity: 1;
        }}

        .main-content {{
            flex: 1;
            overflow-y: auto;
            padding: 64px;
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }}

        .log-container {{
            width: 100%;
            max-width: 900px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 48px;
            /* subtle shadow on rest */
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
            transition: all 0.2s;
            opacity: 0;
            transform: translateY(10px);
            animation: fadeUp 0.4s forwards ease-out;
        }}

        @keyframes fadeUp {{
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .log-container:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        }}

        .markdown-body {{
            font-size: 15px;
            line-height: 1.7;
            color: var(--text-primary);
        }}

        .markdown-body h2 {{
            font-size: 32px;
            margin-top: 0;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 32px;
        }}

        .markdown-body h3 {{
            font-size: 18px;
            margin-top: 40px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
        }}

        /* Style the User and AI headers distinctly */
        .markdown-body h3:contains("👤") {{
            color: var(--text-secondary);
        }}

        .markdown-body h3:contains("🤖") {{
            color: var(--primary);
        }}

        .markdown-body p {{
            margin-bottom: 16px;
        }}

        .markdown-body hr {{
            border: 0;
            height: 1px;
            background: var(--border);
            margin: 32px 0;
        }}

        .markdown-body code {{
            font-family: var(--font-code);
            background: var(--bg);
            padding: 3px 6px;
            border-radius: 4px;
            font-size: 13px;
            border: 1px solid var(--border);
        }}

        .markdown-body pre {{
            background: var(--bg);
            border: 1px solid var(--border);
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 24px 0;
        }}

        .markdown-body pre code {{
            background: transparent;
            padding: 0;
            border: none;
            font-size: 13px;
        }}

        .markdown-body blockquote {{
            border-left: 4px solid var(--primary);
            margin: 24px 0;
            padding: 12px 20px;
            background: var(--bg);
            border-radius: 0 6px 6px 0;
            color: var(--text-secondary);
        }}

        .markdown-body a {{
            color: var(--primary);
            text-decoration: none;
            font-weight: 500;
        }}

        .markdown-body a:hover {{
            color: var(--primary-hover);
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="brand-header">
            <h1>{t['title']}</h1>
            <p>{t['subtitle']}</p>
        </div>
        <div id="date-list"></div>
    </div>
    
    <div class="main-content">
        <div class="log-container" id="content-container">
            <div class="markdown-body" id="markdown-viewer">
                <!-- Content injected here -->
            </div>
        </div>
    </div>

    <script>
        const logs = {logs_json};
        const dates = {json.dumps(dates)};
        const noLogsMsg = "{t['no_logs']}";
        
        const dateListEl = document.getElementById('date-list');
        const viewerEl = document.getElementById('markdown-viewer');
        const containerEl = document.getElementById('content-container');

        // Configure marked.js to handle newlines nicely
        marked.setOptions({{
            breaks: true,
            gfm: true
        }});

        function selectDate(date) {{
            // Update active state
            document.querySelectorAll('.date-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            document.getElementById('btn-' + date).classList.add('active');
            
            // Re-trigger animation
            containerEl.style.animation = 'none';
            containerEl.offsetHeight; /* trigger reflow */
            containerEl.style.animation = null; 

            // Render markdown
            const rawMd = logs[date];
            viewerEl.innerHTML = marked.parse(rawMd);
        }}

        // Initialize sidebar
        dates.forEach((date, index) => {{
            const btn = document.createElement('button');
            btn.className = 'date-btn';
            btn.id = 'btn-' + date;
            btn.textContent = date;
            btn.onclick = () => selectDate(date);
            dateListEl.appendChild(btn);
        }});

        // Load first date by default
        if (dates.length > 0) {{
            selectDate(dates[0]);
        }} else {{
            viewerEl.innerHTML = "<h2 style='text-align:center; color:var(--text-secondary); margin-top: 100px;'>" + noLogsMsg + "</h2>";
        }}
    </script>
</body>
</html>"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Viewer generated at: {os.path.abspath(output_file)}")
    webbrowser.open('file://' + os.path.abspath(output_file))

if __name__ == "__main__":
    generate_viewer()
