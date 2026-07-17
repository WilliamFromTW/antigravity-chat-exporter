import os
import glob
import json
import webbrowser
import urllib.request

I18N = {
    "en": {
        "title": "Explore Log Viewer",
        "subtitle": "Antigravity Chat Exporter",
        "no_logs": "No data found.",
        "html_title": "Genesis Explore Log Viewer",
        "prompt_log_dir": "Default directory not found.\nPlease enter the path to the chat logs directory: ",
        "invalid_log_dir": "Error: Directory does not exist or no files found.",
        "success_msg": "Viewer generated at: ",
        "saved_msg": ">> Directory saved for future use: ",
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
        "prompt_log_dir": "找不到預設目錄。\n請輸入對話日誌的目錄路徑: ",
        "invalid_log_dir": "錯誤：目錄不存在，或找不到任何檔案。",
        "success_msg": "閱讀器已生成於: ",
        "saved_msg": ">> 已記住此目錄，下次將自動讀取: ",
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
        "prompt_log_dir": "找不到默认目录。\n请输入对话日志的目录路径: ",
        "invalid_log_dir": "错误：目录不存在，或找不到任何文件。",
        "success_msg": "阅读器已生成于: ",
        "saved_msg": ">> 已记住此目录，下次将自动读取: ",
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
        "prompt_log_dir": "Không tìm thấy thư mục mặc định.\nVui lòng nhập đường dẫn đến thư mục nhật ký: ",
        "invalid_log_dir": "Lỗi: Thư mục không tồn tại hoặc không tìm thấy tệp.",
        "success_msg": "Trình xem được tạo tại: ",
        "saved_msg": ">> Thư mục đã được lưu cho lần sử dụng sau: ",
        "cat_logs": "Nhật ký",
        "cat_active": "Thay đổi Đang hoạt động",
        "cat_archived": "Thay đổi Đã lưu trữ",
        "search_placeholder": "Tìm kiếm nhật ký và tài liệu..."
    }
}

CONFIG_FILE = ".viewer_config.json"

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

def get_log_dir(t):
    default_dir = "openspec/explorations"
    saved_dir = None
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                saved_dir = config.get("saved_log_dir")
        except:
            pass

    if saved_dir and os.path.exists(saved_dir):
        return saved_dir
        
    if os.path.exists(default_dir):
        return default_dir
        
    user_dir = input(t["prompt_log_dir"]).strip()
    if not user_dir or not os.path.exists(user_dir):
        print(t["invalid_log_dir"])
        return None
        
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"saved_log_dir": user_dir}, f)
        print(t["saved_msg"] + user_dir)
    except:
        pass
        
    return user_dir

def parse_change_dir(change_dir):
    change_data = {}
    for root, _, files in os.walk(change_dir):
        for f in files:
            if f.endswith('.md'):
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, change_dir).replace('\\', '/')
                with open(abs_path, 'r', encoding='utf-8') as file:
                    change_data[rel_path] = file.read()
    return change_data

def generate_viewer():
    lang = choose_language()
    t = I18N[lang]
    
    output_file = "chat_history_viewer.html"
    log_dir = get_log_dir(t)
    
    if not log_dir:
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
                project_data["logs"][date_str] = {
                    "content": file.read(),
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
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="brand-header">
            <h1 data-i18n="title">__TITLE__</h1>
            <p data-i18n="subtitle">__SUBTITLE__</p>
        </div>
        <input type="text" class="search-box" id="search-input" placeholder="__SEARCH_PLACEHOLDER__" data-i18n-placeholder="search_placeholder">
        <div id="navigation"></div>
        <div style="flex-grow: 1;"></div>
        <select id="lang-selector" onchange="applyTranslations(this.value)" style="margin-top: 24px; width: 100%; padding: 8px; border-radius: 6px; border: 1px solid var(--border); background: var(--bg); font-family: var(--font-body); font-size: 13px; color: var(--text-secondary); cursor: pointer; outline: none;">
            <option value="en">English</option>
            <option value="zh-tw">繁體中文</option>
            <option value="zh-cn">简体中文</option>
            <option value="vi">Tiếng Việt</option>
        </select>
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
        let detectedLang = navigator.language.toLowerCase();
        if (!i18nDict[detectedLang]) {
            if (detectedLang.startsWith('zh-cn') || detectedLang.startsWith('zh-hans')) detectedLang = 'zh-cn';
            else if (detectedLang.startsWith('zh')) detectedLang = 'zh-tw';
            else if (detectedLang.startsWith('vi')) detectedLang = 'vi';
            else detectedLang = 'en';
        }
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
                    logsHtml += `<button class="nav-item log-nav" onclick="selectLog('${date}')">📄 ${date}</button>`;
                }
            });
            if (logsHtml) navEl.innerHTML += `<div class="category-header" onclick="toggleCat(this)">${TEXT_CAT_LOGS}</div><div class="category-content">${logsHtml}</div>`;

            // Active Changes
            const activeChanges = Object.keys(projectData.active_changes).sort();
            let activeHtml = "";
            activeChanges.forEach(change => {
                let filesHtml = "";
                const files = Object.keys(projectData.active_changes[change]).sort();
                let folderMatches = change.toLowerCase().includes(currentSearch);
                files.forEach(f => {
                    if (folderMatches || matchesSearch(projectData.active_changes[change][f], currentSearch) || f.toLowerCase().includes(currentSearch)) {
                        filesHtml += `<button class="nav-item file-nav" onclick="selectArtifact('active_changes', '${change}', '${f}')">📄 ${f}</button>`;
                    }
                });
                if (filesHtml) {
                    activeHtml += `<div class="nav-folder-title">${change}</div><div class="nav-folder">${filesHtml}</div>`;
                }
            });
            if (activeHtml) navEl.innerHTML += `<div class="category-header" onclick="toggleCat(this)">${TEXT_CAT_ACTIVE}</div><div class="category-content">${activeHtml}</div>`;

            // Archived Changes
            const archivedChanges = Object.keys(projectData.archived_changes).sort().reverse();
            let archivedHtml = "";
            archivedChanges.forEach(change => {
                let filesHtml = "";
                const files = Object.keys(projectData.archived_changes[change]).sort();
                let folderMatches = change.toLowerCase().includes(currentSearch);
                files.forEach(f => {
                    if (folderMatches || matchesSearch(projectData.archived_changes[change][f], currentSearch) || f.toLowerCase().includes(currentSearch)) {
                        filesHtml += `<button class="nav-item file-nav" onclick="selectArtifact('archived_changes', '${change}', '${f}')">📄 ${f}</button>`;
                    }
                });
                if (filesHtml) {
                    archivedHtml += `<div class="nav-folder-title">${change}</div><div class="nav-folder">${filesHtml}</div>`;
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
                if (b.textContent.includes(file) && b.parentElement.previousElementSibling.textContent.includes(change)) b.classList.add('active'); 
            });
            triggerAnimation();
            const rawMd = projectData[category][change][file];
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
                const files = Object.keys(projectData.active_changes[changeName]).sort();
                if (files.length > 0) selectArtifact('active_changes', changeName, files.includes('proposal.md') ? 'proposal.md' : files[0]);
            } else if (projectData.archived_changes[changeName]) {
                const files = Object.keys(projectData.archived_changes[changeName]).sort();
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
                const f = Object.keys(projectData.active_changes[firstActive]).sort()[0];
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

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"{t['success_msg']}{os.path.abspath(output_file)}")
    webbrowser.open('file://' + os.path.abspath(output_file))

if __name__ == "__main__":
    generate_viewer()
