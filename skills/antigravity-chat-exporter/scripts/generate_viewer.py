import os
import glob
import json
import webbrowser
import urllib.request
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Force the working directory to the project root
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
os.chdir(ROOT_DIR)

I18N = {
    "en": {
        "title": "Explore Log Viewer",
        "subtitle": "Antigravity Chat Exporter",
        "no_logs": "No data found.",
        "html_title": "Genesis Explore Log Viewer",
        "success_msg": "Viewer generated at: ",
        "cat_logs": "Logs",
        "cat_active": "Active Changes",
        "cat_archived": "Archived Changes",
        "search_placeholder": "Search logs and artifacts..."
    },
    "zh-tw": {
        "title": "對話探索日誌",
        "subtitle": "Antigravity 對話匯出器",
        "no_logs": "找不到任何資料。",
        "html_title": "Genesis 對話探索日誌",
        "success_msg": "閱讀器已生成於: ",
        "cat_logs": "對話日誌",
        "cat_active": "活躍變更",
        "cat_archived": "封存變更",
        "search_placeholder": "搜尋日誌與專案文件..."
    },
    "zh-cn": {
        "title": "对话探索日志",
        "subtitle": "Antigravity 对话导出器",
        "no_logs": "找不到任何资料。",
        "html_title": "Genesis 对话探索日志",
        "success_msg": "阅读器已生成于: ",
        "cat_logs": "对话日志",
        "cat_active": "活跃变更",
        "cat_archived": "归档变更",
        "search_placeholder": "搜索日志与项目文件..."
    },
    "vi": {
        "title": "Nhật ký Khám phá Trò chuyện",
        "subtitle": "Trình xuất trò chuyện Antigravity",
        "no_logs": "Không tìm thấy dữ liệu.",
        "html_title": "Genesis Nhật ký Khám phá Trò chuyện",
        "success_msg": "Trình xem được tạo tại: ",
        "cat_logs": "Nhật ký",
        "cat_active": "Thay đổi Đang hoạt động",
        "cat_archived": "Thay đổi Đã lưu trữ",
        "search_placeholder": "Tìm kiếm nhật ký và tài liệu..."
    }
}

def get_marked_js_source():
    cache_file = ".marked.min.js.cache"
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return f.read()
        except:
            pass
    
    url = "https://cdn.jsdelivr.net/npm/marked/marked.min.js"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        js_code = response.read().decode('utf-8')
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(js_code)
        return js_code
    except Exception as e:
        print(f"Failed to fetch marked.js: {e}")
        return "/* Failed to load marked.js */"

def get_changes_i18n():
    i18n_file = "openspec/changes_i18n.json"
    if os.path.exists(i18n_file):
        try:
            with open(i18n_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

CHANGES_I18N_DICT = get_changes_i18n()

def parse_change_dir(change_dir):
    change_data = {"files": {}}
    title_zh = ""
    title_zh_cn = ""
    title_vi = ""
    change_name = os.path.basename(change_dir)
    clean_name = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', change_name)
    title_en = " ".join(word.capitalize() for word in clean_name.split('-'))
    
    # Dictionary lookup
    if clean_name in CHANGES_I18N_DICT:
        title_zh = CHANGES_I18N_DICT[clean_name].get("zh-tw", "")
        title_en = CHANGES_I18N_DICT[clean_name].get("en", title_en)
        title_zh_cn = CHANGES_I18N_DICT[clean_name].get("zh-cn", "")
        title_vi = CHANGES_I18N_DICT[clean_name].get("vi", "")
            
    for root, _, files in os.walk(change_dir):
        for f in files:
            if f.endswith('.md'):
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, change_dir).replace('\\', '/')
                with open(abs_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    change_data["files"][rel_path] = content
                    # Fallback to proposal if not in i18n
                    if not title_zh and rel_path == "proposal.md":
                        first_line = content.strip().split('\n')[0]
                        if first_line.startswith("# "):
                            title_zh = first_line[2:].strip()
                            
    change_data["title_zh"] = title_zh if title_zh else title_en
    change_data["title_zh_cn"] = title_zh_cn if title_zh_cn else change_data["title_zh"]
    change_data["title_vi"] = title_vi if title_vi else title_en
    change_data["title_en"] = title_en
    return change_data

def generate_viewer():
    lang = "en"
    t = I18N[lang]
    
    output_file = "chat_history_viewer.html"
    log_dir = "openspec/explorations"
    
    if not os.path.exists(log_dir):
        print(t.get("no_logs", "No logs"))
        return

    md_files = glob.glob(os.path.join(log_dir, "explore_log_*.md"))
    if not md_files:
        md_files = glob.glob(os.path.join(log_dir, "*.md"))
        
    project_data = {
        "logs": {},
        "active_changes": {},
        "archived_changes": {}
    }

    if md_files:
        for f in md_files:
            filename = os.path.basename(f)
            date_str = filename.replace('explore_log_', '').replace('.md', '')
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                summary_match = re.search(r'> \[!NOTE\]\s*> \*\*.*?(?:Summary|摘要|總結).*?\*\*\s*(>.*?)(?=\n\n|\Z)', content, re.IGNORECASE | re.DOTALL)
                summary = ""
                if summary_match:
                    summary = re.sub(r'^>\s?', '', summary_match.group(1), flags=re.MULTILINE).strip()
                project_data["logs"][date_str] = {
                    "content": content,
                    "summary": summary,
                    "related_changes": []
                }

    changes_dir = "openspec/changes"
    if os.path.exists(changes_dir):
        for entry in os.listdir(changes_dir):
            entry_path = os.path.join(changes_dir, entry)
            if os.path.isdir(entry_path) and entry != "archive":
                project_data["active_changes"][entry] = parse_change_dir(entry_path)

    archive_dir = os.path.join(changes_dir, "archive")
    if os.path.exists(archive_dir):
        for entry in os.listdir(archive_dir):
            entry_path = os.path.join(archive_dir, entry)
            if os.path.isdir(entry_path):
                project_data["archived_changes"][entry] = parse_change_dir(entry_path)
                
    all_change_names = list(project_data["active_changes"].keys()) + list(project_data["archived_changes"].keys())
    for date_str, log_obj in project_data["logs"].items():
        content = log_obj["content"]
        for change_name in all_change_names:
            if change_name in content:
                log_obj["related_changes"].append(change_name)

    if not project_data["logs"] and not project_data["active_changes"] and not project_data["archived_changes"]:
        print(t["invalid_log_dir"])
        return

    project_data_json = json.dumps(project_data).replace("</", "<\\/")

    # Use raw string for HTML template to avoid syntax issues with formatting
    html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__HTML_TITLE__</title>
    <!-- Genesis Typography -->
    <link href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <!-- Marked.js for Markdown parsing -->
    <script>__MARKED_JS__</script>
    
    <style>
        :root {
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
        }

        * { box-sizing: border-box; }
        body {
            margin: 0; padding: 0; background-color: var(--bg); color: var(--text-primary);
            font-family: var(--font-body); display: flex; height: 100vh; overflow: hidden;
        }
        h1, h2, h3, h4, h5, h6 { font-family: var(--font-display); font-weight: 700; letter-spacing: -0.03em; }
        
        .sidebar {
            width: 320px; background: var(--surface); border-right: 1px solid var(--border);
            display: flex; flex-direction: column; padding: 32px 24px; overflow-y: auto; z-index: 10;
        }
        .brand-header { margin-bottom: 24px; }
        .brand-header h1 { font-size: 24px; margin: 0; }
        .brand-header p { color: var(--text-secondary); font-size: 13px; margin: 4px 0 0 0; }
        
        .search-box {
            width: 100%; padding: 10px 14px; border-radius: 6px; border: 1px solid var(--border);
            background: var(--bg); margin-bottom: 24px; font-family: var(--font-body); font-size: 14px;
        }
        .search-box:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(99,102,241,0.12); }
        
        .category-header {
            font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
            color: var(--text-secondary); margin-top: 24px; margin-bottom: 12px; display: flex;
            align-items: center; cursor: pointer; user-select: none;
        }
        .category-header::before { content: "▼"; font-size: 9px; margin-right: 8px; transition: transform 0.2s; }
        .category-header.collapsed::before { transform: rotate(-90deg); }
        .category-content { display: block; }
        .category-content.collapsed { display: none; }
        
        .nav-item {
            background: transparent; border: 1px solid transparent; text-align: left; padding: 8px 12px;
            border-radius: 6px; font-family: var(--font-body); font-size: 14px; font-weight: 500;
            color: var(--text-secondary); cursor: pointer; margin-bottom: 4px; transition: all 0.2s;
            display: flex; align-items: center; width: 100%;
        }
        .nav-item:hover { background: var(--bg); color: var(--text-primary); }
        .nav-item.active { background: var(--primary); color: var(--surface); }
        .nav-folder { margin-left: 12px; padding-left: 12px; border-left: 1px solid var(--border); margin-bottom: 8px; }
        .nav-folder-title { font-size: 13px; font-weight: 600; color: var(--text-primary); margin: 8px 0 4px 0; display: flex; align-items: center; }
        .nav-folder-title::before { content: "📂"; margin-right: 6px; font-size: 12px; }
        
        .main-content { flex: 1; overflow-y: auto; padding: 64px; display: flex; justify-content: center; align-items: flex-start; }
        .log-container {
            width: 100%; max-width: 900px; background: var(--surface); border: 1px solid var(--border);
            border-radius: 12px; padding: 48px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);
            animation: fadeUp 0.4s forwards ease-out;
        }
        @keyframes fadeUp { from {opacity:0; transform:translateY(10px);} to {opacity:1; transform:translateY(0);} }
        
        mark { background-color: #FEF08A; color: #854D0E; padding: 2px 4px; border-radius: 3px; }
        .related-tags { margin-bottom: 24px; display: flex; gap: 8px; flex-wrap: wrap; }
        .related-tag {
            background: #EEF2FF; color: var(--primary-hover); border: 1px solid #C7D2FE;
            padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; cursor: pointer;
        }
        .related-tag:hover { background: #E0E7FF; }
        
        .markdown-body { font-size: 15px; line-height: 1.7; color: var(--text-primary); }
        .markdown-body h2 { font-size: 32px; margin-top: 0; padding-bottom: 16px; border-bottom: 1px solid var(--border); margin-bottom: 32px; }
        .markdown-body h3 { font-size: 18px; margin-top: 40px; margin-bottom: 16px; display: flex; align-items: center; }
        .markdown-body h3:contains("👤") { color: var(--text-secondary); }
        .markdown-body h3:contains("🤖") { color: var(--primary); }
        .markdown-body code { font-family: var(--font-code); background: var(--bg); padding: 3px 6px; border-radius: 4px; font-size: 13px; border: 1px solid var(--border); }
        .markdown-body pre { background: var(--bg); border: 1px solid var(--border); padding: 20px; border-radius: 8px; overflow-x: auto; margin: 24px 0; }
        .markdown-body pre code { background: transparent; padding: 0; border: none; }
        .markdown-body blockquote { border-left: 4px solid var(--primary); margin: 24px 0; padding: 12px 20px; background: var(--bg); border-radius: 0 6px 6px 0; color: var(--text-secondary); }
        /* EARS Syntax Highlighting */
        .ears-keyword { font-weight: 700; font-family: var(--font-code); padding: 1px 4px; border-radius: 3px; font-size: 13px; }
        .ears-when, .ears-where, .ears-if { background: #E0F2FE; color: #0284C7; border: 1px solid #BAE6FD; }
        .ears-while { background: #CCFBF1; color: #0D9488; border: 1px solid #99F6E4; }
        .ears-then, .ears-shall { background: #FEE2E2; color: #DC2626; border: 1px solid #FECACA; }
        
        /* Task List Completion Highlighting (Checkbox only) */
        .markdown-body input[type="checkbox"] {
            pointer-events: none; /* Prevent clicking since we will remove 'disabled' attribute */
        }
        .markdown-body input[type="checkbox"]:checked {
            accent-color: #10B981; /* Emerald green */
            transform: scale(1.15); /* Slightly enlarge to make it pop */
            transition: all 0.2s;
        }
        
        /* Sidebar Summary Preview */
        .log-nav-wrapper { display: flex; flex-direction: column; }
        .sidebar-summary { font-size: 12px; color: var(--text-secondary); background: #F8FAFC; margin: 0 16px 8px 16px; padding: 10px; border-radius: 6px; border: 1px solid #E2E8F0; overflow-y: auto; max-height: 300px; transition: max-height 0.3s ease, opacity 0.3s ease, padding 0.3s ease, margin 0.3s ease; }
        .sidebar-summary.collapsed { max-height: 0; opacity: 0; padding-top: 0; padding-bottom: 0; margin-top: 0; margin-bottom: 0; border: none; overflow: hidden; }
        .sidebar-summary p { margin: 4px 0; }
        
        /* I18N Language Filtering */
        body [lang="zh-tw"], body [lang="zh-cn"], body [lang="vi"], body [lang="en"] {
            display: none !important;
        }
        body.lang-en [lang="en"] { display: block !important; }
        body.lang-zh-tw [lang="zh-tw"] { display: block !important; }
        body.lang-zh-cn [lang="zh-cn"] { display: block !important; }
        body.lang-vi [lang="vi"] { display: block !important; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="brand-header">
            <h1 data-i18n="title">__TITLE__</h1>
            <p data-i18n="subtitle">__SUBTITLE__</p>
            <select id="lang-selector" onchange="applyTranslations(this.value)" style="margin-top: 16px; width: 100%; padding: 8px; border-radius: 6px; border: 1px solid var(--border); background: var(--bg); font-family: var(--font-body); font-size: 13px; color: var(--text-secondary); cursor: pointer; outline: none;">
                <option value="en">English</option>
                <option value="zh-tw">繁體中文</option>
                <option value="zh-cn">简体中文</option>
                <option value="vi">Tiếng Việt</option>
            </select>
        </div>
        <input type="text" class="search-box" id="search-input" placeholder="__SEARCH_PLACEHOLDER__" data-i18n-placeholder="search_placeholder">
        <div id="navigation"></div>
        <div style="flex-grow: 1;"></div>
    </div>
    
    <div class="main-content">
        <div class="log-container" id="content-container">
            <div class="markdown-body" id="markdown-viewer"></div>
        </div>
    </div>

    <script>
        const projectData = __PROJECT_DATA__;
        const i18nDict = __I18N_DICT__;
        const noLogsMsg = "__NO_LOGS__";
        let currentSearch = "";

        const navEl = document.getElementById('navigation');
        const searchEl = document.getElementById('search-input');
        const viewerEl = document.getElementById('markdown-viewer');
        const containerEl = document.getElementById('content-container');

        let TEXT_CAT_LOGS = "__CAT_LOGS__";
        let TEXT_CAT_ACTIVE = "__CAT_ACTIVE__";
        let TEXT_CAT_ARCHIVED = "__CAT_ARCHIVED__";

        window.applyTranslations = function(lang) {
            document.body.className = 'lang-' + lang;
            const t = i18nDict[lang] || i18nDict['en'];
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (t[key]) el.textContent = t[key];
            });
            document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
                const key = el.getAttribute('data-i18n-placeholder');
                if (t[key]) el.placeholder = t[key];
            });
            TEXT_CAT_LOGS = t['cat_logs'];
            TEXT_CAT_ACTIVE = t['cat_active'];
            TEXT_CAT_ARCHIVED = t['cat_archived'];
            
            if (navEl.innerHTML.trim() !== '') {
                renderNav();
            }
            
            const selector = document.getElementById('lang-selector');
            if (selector && selector.value !== lang) {
                selector.value = lang;
            }
        };

        // Initialize translation
        let detectedLang = "__DEFAULT_LANG__";
        applyTranslations(detectedLang);

        marked.setOptions({ breaks: true, gfm: true });

        function matchesSearch(content, query) {
            if (!query) return true;
            return content.toLowerCase().includes(query);
        }

        window.toggleCat = function(el) {
            el.classList.toggle('collapsed');
            el.nextElementSibling.classList.toggle('collapsed');
        }

        window.toggleSummary = function(date, event) {
            if (event) {
                event.stopPropagation();
            }
            const el = document.getElementById('summary-' + date);
            if (el) {
                el.classList.toggle('collapsed');
            }
        }

        function highlightText(html, query) {
            if (!query) return html;
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;
            // Escape regex special characters
            const escapedQuery = query.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
            const regex = new RegExp("(" + escapedQuery + ")", "gi");
            
            function highlightNodes(node) {
                if (node.nodeType === 3) {
                    const matches = node.nodeValue.match(regex);
                    if (matches) {
                        const wrapper = document.createElement('span');
                        wrapper.innerHTML = node.nodeValue.replace(regex, "<mark>$1</mark>");
                        node.parentNode.replaceChild(wrapper, node);
                    }
                } else if (node.nodeType === 1 && node.nodeName !== 'SCRIPT' && node.nodeName !== 'STYLE' && node.nodeName !== 'MARK') {
                    Array.from(node.childNodes).forEach(highlightNodes);
                }
            }
            Array.from(tempDiv.childNodes).forEach(highlightNodes);
            return tempDiv.innerHTML;
        }

        function renderNav() {
            navEl.innerHTML = "";
            
            // Logs
            const logDates = Object.keys(projectData.logs).sort().reverse();
            let logsHtml = "";
            logDates.forEach(date => {
                if (matchesSearch(projectData.logs[date].content, currentSearch) || date.toLowerCase().includes(currentSearch)) {
                    let summaryHtml = "";
                    if (projectData.logs[date].summary) {
                        summaryHtml = `<div class="sidebar-summary" id="summary-${date}">${marked.parse(projectData.logs[date].summary)}</div>`;
                    }
                    logsHtml += `
                        <div class="log-nav-wrapper">
                            <button class="nav-item log-nav" onclick="selectLog('${date}'); toggleSummary('${date}', event)">📄 ${date}</button>
                            ${summaryHtml}
                        </div>`;
                }
            });
            if (logsHtml) navEl.innerHTML += `<div class="category-header" onclick="toggleCat(this)">${TEXT_CAT_LOGS}</div><div class="category-content">${logsHtml}</div>`;

            // Active Changes
            const activeChanges = Object.keys(projectData.active_changes).sort();
            let activeHtml = "";
            activeChanges.forEach(change => {
                let filesHtml = "";
                const changeObj = projectData.active_changes[change];
                let changeTitle = changeObj.title_en || change;
                if (document.body.className.includes('lang-zh-tw')) {
                    changeTitle = changeObj.title_zh || changeTitle;
                } else if (document.body.className.includes('lang-zh-cn')) {
                    changeTitle = changeObj.title_zh_cn || changeTitle;
                } else if (document.body.className.includes('lang-vi')) {
                    changeTitle = changeObj.title_vi || changeTitle;
                }
                
                const customOrder = ['proposal.md', 'design.md', 'tasks.md', 'specs'];
                const files = Object.keys(changeObj.files).sort((a, b) => {
                    let idxA = customOrder.findIndex(o => a.startsWith(o));
                    let idxB = customOrder.findIndex(o => b.startsWith(o));
                    if (idxA === -1) idxA = 999;
                    if (idxB === -1) idxB = 999;
                    if (idxA !== idxB) return idxA - idxB;
                    return a.localeCompare(b);
                });
                
                let folderMatches = change.toLowerCase().includes(currentSearch) || changeTitle.toLowerCase().includes(currentSearch);
                files.forEach(f => {
                    if (folderMatches || matchesSearch(changeObj.files[f], currentSearch) || f.toLowerCase().includes(currentSearch)) {
                        filesHtml += `<button class="nav-item file-nav" onclick="selectArtifact('active_changes', '${change}', '${f}')">📄 ${f}</button>`;
                    }
                });
                if (filesHtml) {
                    activeHtml += `<div class="nav-folder-title" title="${change}">${changeTitle}</div><div class="nav-folder">${filesHtml}</div>`;
                }
            });
            if (activeHtml) navEl.innerHTML += `<div class="category-header" onclick="toggleCat(this)">${TEXT_CAT_ACTIVE}</div><div class="category-content">${activeHtml}</div>`;

            // Archived Changes
            const archivedChanges = Object.keys(projectData.archived_changes).sort().reverse();
            let archivedHtml = "";
            archivedChanges.forEach(change => {
                let filesHtml = "";
                const changeObj = projectData.archived_changes[change];
                let changeTitle = changeObj.title_en || change;
                if (document.body.className.includes('lang-zh-tw')) {
                    changeTitle = changeObj.title_zh || changeTitle;
                } else if (document.body.className.includes('lang-zh-cn')) {
                    changeTitle = changeObj.title_zh_cn || changeTitle;
                } else if (document.body.className.includes('lang-vi')) {
                    changeTitle = changeObj.title_vi || changeTitle;
                }
                
                const customOrder = ['proposal.md', 'design.md', 'tasks.md', 'specs'];
                const files = Object.keys(changeObj.files).sort((a, b) => {
                    let idxA = customOrder.findIndex(o => a.startsWith(o));
                    let idxB = customOrder.findIndex(o => b.startsWith(o));
                    if (idxA === -1) idxA = 999;
                    if (idxB === -1) idxB = 999;
                    if (idxA !== idxB) return idxA - idxB;
                    return a.localeCompare(b);
                });
                
                let folderMatches = change.toLowerCase().includes(currentSearch) || changeTitle.toLowerCase().includes(currentSearch);
                files.forEach(f => {
                    if (folderMatches || matchesSearch(changeObj.files[f], currentSearch) || f.toLowerCase().includes(currentSearch)) {
                        filesHtml += `<button class="nav-item file-nav" onclick="selectArtifact('archived_changes', '${change}', '${f}')">📄 ${f}</button>`;
                    }
                });
                if (filesHtml) {
                    archivedHtml += `<div class="nav-folder-title" title="${change}">${changeTitle}</div><div class="nav-folder">${filesHtml}</div>`;
                }
            });
            if (archivedHtml) navEl.innerHTML += `<div class="category-header collapsed" onclick="toggleCat(this)">${TEXT_CAT_ARCHIVED}</div><div class="category-content collapsed">${archivedHtml}</div>`;
        }

        function triggerAnimation() {
            containerEl.style.animation = 'none';
            containerEl.offsetHeight; 
            containerEl.style.animation = null; 
        }

        function clearActiveNav() {
            document.querySelectorAll('.nav-item').forEach(btn => btn.classList.remove('active'));
        }

        function escapeHTML(str) {
            return str.replace(/[&<>'"]/g, tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag]));
        }

        function applyEarsHighlighting(element) {
            const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
            const nodesToReplace = [];
            let node;
            while (node = walker.nextNode()) {
                let parent = node.parentNode;
                let skip = false;
                while (parent && parent !== element) {
                    if (parent.tagName === 'PRE' || parent.tagName === 'CODE') {
                        skip = true;
                        break;
                    }
                    parent = parent.parentNode;
                }
                if (!skip) {
                    nodesToReplace.push(node);
                }
            }

            const regex = /\b(WHEN|WHILE|WHERE|IF|THEN|SHALL)\b/g;
            nodesToReplace.forEach(n => {
                if (regex.test(n.nodeValue)) {
                    const span = document.createElement('span');
                    span.innerHTML = escapeHTML(n.nodeValue).replace(regex, (match) => {
                        return `<span class="ears-keyword ears-${match.toLowerCase()}">${match}</span>`;
                    });
                    n.parentNode.replaceChild(span, n);
                }
            });
        }

        window.selectLog = function(date) {
            clearActiveNav();
            document.querySelectorAll('.log-nav').forEach(b => { if (b.textContent.includes(date)) b.classList.add('active'); });
            triggerAnimation();
            const logData = projectData.logs[date];
            let headerHtml = "";
            if (logData.related_changes && logData.related_changes.length > 0) {
                let tags = logData.related_changes.map(c => `<span class="related-tag" onclick="jumpToChange('${c}')">🔗 ${c}</span>`).join('');
                headerHtml = `<div class="related-tags">${tags}</div>`;
            }
            let html = marked.parse(logData.content);
            if (currentSearch) html = highlightText(html, currentSearch);
            viewerEl.innerHTML = headerHtml + html;
            viewerEl.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.removeAttribute('disabled'));
        }

        window.selectArtifact = function(category, change, file) {
            clearActiveNav();
            document.querySelectorAll('.file-nav').forEach(b => { 
                if (b.textContent.includes(file) && b.parentElement.previousElementSibling.getAttribute('title') === change) b.classList.add('active'); 
            });
            triggerAnimation();
            const rawMd = projectData[category][change].files[file];
            let html = marked.parse(rawMd);
            if (currentSearch) html = highlightText(html, currentSearch);
            viewerEl.innerHTML = html;
            viewerEl.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.removeAttribute('disabled'));
            applyEarsHighlighting(viewerEl);
        }

        window.jumpToChange = function(changeName) {
            document.querySelectorAll('.category-header').forEach(h => {
                h.classList.remove('collapsed');
                h.nextElementSibling.classList.remove('collapsed');
            });
            searchEl.value = changeName;
            currentSearch = changeName.toLowerCase();
            renderNav();
            
            if (projectData.active_changes[changeName]) {
                const files = Object.keys(projectData.active_changes[changeName].files).sort();
                if (files.length > 0) selectArtifact('active_changes', changeName, files.includes('proposal.md') ? 'proposal.md' : files[0]);
            } else if (projectData.archived_changes[changeName]) {
                const files = Object.keys(projectData.archived_changes[changeName].files).sort();
                if (files.length > 0) selectArtifact('archived_changes', changeName, files.includes('proposal.md') ? 'proposal.md' : files[0]);
            }
        }

        searchEl.addEventListener('input', (e) => {
            currentSearch = e.target.value.toLowerCase().trim();
            renderNav();
        });

        renderNav();
        const firstLog = Object.keys(projectData.logs).sort().reverse()[0];
        if (firstLog) {
            selectLog(firstLog);
        } else {
            const firstActive = Object.keys(projectData.active_changes).sort()[0];
            if (firstActive) {
                const f = Object.keys(projectData.active_changes[firstActive].files).sort()[0];
                selectArtifact('active_changes', firstActive, f);
            } else {
                viewerEl.innerHTML = "<h2 style='text-align:center; color:var(--text-secondary); margin-top: 100px;'>" + noLogsMsg + "</h2>";
            }
        }
    </script>
</body>
</html>"""

    html_content = html_template.replace("__HTML_TITLE__", t['html_title'])
    html_content = html_content.replace("__MARKED_JS__", get_marked_js_source())
    html_content = html_content.replace("__I18N_DICT__", json.dumps(I18N).replace("</", "<\\/"))
    html_content = html_content.replace("__TITLE__", t['title'])
    html_content = html_content.replace("__SUBTITLE__", t['subtitle'])
    html_content = html_content.replace("__NO_LOGS__", t['no_logs'])
    html_content = html_content.replace("__PROJECT_DATA__", project_data_json)
    html_content = html_content.replace("__SEARCH_PLACEHOLDER__", t['search_placeholder'])
    html_content = html_content.replace("__CAT_LOGS__", t['cat_logs'])
    html_content = html_content.replace("__CAT_ACTIVE__", t['cat_active'])
    html_content = html_content.replace("__CAT_ARCHIVED__", t['cat_archived'])
    html_content = html_content.replace("__DEFAULT_LANG__", lang)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"{t['success_msg']}{os.path.abspath(output_file)}")
    webbrowser.open('file://' + os.path.abspath(output_file))

if __name__ == "__main__":
    generate_viewer()
