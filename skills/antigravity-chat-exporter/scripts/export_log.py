import argparse
import json
import os
import datetime
import re

def export_conversation(app_data_dir, conversation_id, output_dir):
    logs_dir = os.path.join(app_data_dir, "brain", conversation_id, ".system_generated", "logs")
    transcript_path = os.path.join(logs_dir, "transcript_full.jsonl")
    
    if not os.path.exists(transcript_path):
        # Fallback to truncated transcript if full one is not available
        transcript_path = os.path.join(logs_dir, "transcript.jsonl")
        
    if not os.path.exists(transcript_path):
        return False

    # Find the date of the LAST message to determine which daily file to use
    last_date_str = None
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            last_line = None
            for line in f:
                if line.strip():
                    last_line = line
            
            if last_line:
                step = json.loads(last_line)
                created_at = step.get('created_at')
                if created_at:
                    dt = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                    dt_local = dt + datetime.timedelta(hours=8) # Convert to TW time
                    last_date_str = dt_local.strftime("%Y-%m-%d")
    except:
        pass
        
    if not last_date_str:
        last_date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    output_path = os.path.join(output_dir, f"explore_log_{last_date_str}.md")

    # Generate the new conversation content
    markdown_content = f"<!-- CONVERSATION_START: {conversation_id} -->\n"
    markdown_content += f"## 對話與探索紀錄 (Conversation ID: `{conversation_id}`)\n"
    markdown_content += f"更新時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    markdown_content += "---\n\n"

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                try:
                    step = json.loads(line)
                    
                    created_at = step.get('created_at', '')
                    time_str = ""
                    if created_at:
                        try:
                            # Convert 2026-07-09T08:07:29Z to a readable format
                            dt = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                            # Add 8 hours for UTC+8 (Taiwan time)
                            dt_local = dt + datetime.timedelta(hours=8)
                            time_str = f" [{dt_local.strftime('%Y-%m-%d %H:%M:%S')}]"
                        except:
                            time_str = f" [{created_at}]"

                    if step.get('type') == 'USER_INPUT':
                        content = step.get('content', '')
                        req_match = re.search(r'<USER_REQUEST>(.*?)</USER_REQUEST>', content, re.DOTALL)
                        if req_match:
                            content = req_match.group(1).strip()
                        else:
                            content = content.strip()
                            
                        if content:
                            markdown_content += f"### 👤 User{time_str}\n\n" + content + "\n\n---\n\n"
                            
                    elif step.get('type') == 'PLANNER_RESPONSE':
                        content = step.get('content', '')
                        if content:
                            markdown_content += f"### 🤖 AI{time_str}\n\n" + content.strip() + "\n\n---\n\n"
                            
                except json.JSONDecodeError:
                    pass
        
        markdown_content += f"<!-- CONVERSATION_END: {conversation_id} -->\n\n"
        
        # Read existing file to remove previous export of the SAME conversation
        existing_content = ""
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as ef:
                existing_content = ef.read()
                
            # Regex to remove the block of the current conversation if it was exported before
            pattern = rf"<!-- CONVERSATION_START: {conversation_id} -->.*?<!-- CONVERSATION_END: {conversation_id} -->\n*"
            existing_content = re.sub(pattern, "", existing_content, flags=re.DOTALL)

        # Write combined content back
        with open(output_path, 'w', encoding='utf-8') as out:
            if existing_content.strip():
                out.write(existing_content.rstrip() + "\n\n")
            out.write(markdown_content)
            
        print(f"Log exported successfully: {conversation_id} -> {output_path}")
        return True
        
    except Exception as e:
        print(f"Failed to export log {conversation_id}: {e}")
        return False

import shutil
import sqlite3
import json
from pathlib import Path

def backup_brain_state(app_data_dir, conversation_id, project_path):
    agy_root = Path(app_data_dir)
    sync_dir = Path(project_path) / ".antigravity_sync" / "brains"
    
    # Target directories
    dst_uuid_dir = sync_dir / conversation_id
    dst_brain = dst_uuid_dir / "brain"
    
    # 1. Backup brain folder
    src_brain = agy_root / "brain" / conversation_id
    if src_brain.exists() and src_brain.is_dir():
        if dst_brain.exists():
            shutil.rmtree(dst_brain, ignore_errors=True)
        try:
            shutil.copytree(src_brain, dst_brain, ignore=shutil.ignore_patterns('.git'))
            print(f"Backed up brain directory for {conversation_id}")
        except Exception as e:
            print(f"Error copying brain dir {conversation_id}: {e}")
            
    # 2. Backup conversations DB
    src_db = agy_root / "conversations" / f"{conversation_id}.db"
    if src_db.exists():
        dst_db = dst_uuid_dir / "conversations" / f"{conversation_id}.db"
        dst_db.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src_db, dst_db)
            print(f"Backed up db for {conversation_id}")
        except Exception as e:
            print(f"Error copying db {conversation_id}: {e}")
            
    # 3. Backup summary.json
    try:
        summary_db = agy_root / "conversation_summaries.db"
        if summary_db.exists():
            conn = sqlite3.connect(str(summary_db))
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM conversation_summaries WHERE conversation_id=?", (conversation_id,))
            row = c.fetchone()
            if row:
                summary_data = dict(row)
                summary_json_path = dst_uuid_dir / "summary.json"
                summary_json_path.parent.mkdir(parents=True, exist_ok=True)
                with open(summary_json_path, 'w', encoding='utf-8') as f:
                    json.dump(summary_data, f, ensure_ascii=False, indent=2)
                print(f"Backed up summary for {conversation_id}")
            conn.close()
    except Exception as e:
        print(f"Error exporting summary for {conversation_id}: {e}")

import time

def import_brains(app_data_dir, project_path):
    agy_root = Path(app_data_dir)
    sync_dir = Path(project_path) / ".antigravity_sync" / "brains"
    
    if not sync_dir.exists():
        print(f"No sync directory found at {sync_dir}")
        return
        
    imported_count = 0
    for uuid_dir in sync_dir.iterdir():
        if not uuid_dir.is_dir(): continue
        
        conversation_id = uuid_dir.name
        dst_brain = agy_root / "brain" / conversation_id
        
        # 1. Restore brain folder
        src_brain = uuid_dir / "brain"
        if src_brain.exists():
            if dst_brain.exists():
                backup_base = str(agy_root / "brain" / f"{conversation_id}_backup_{int(time.time())}")
                shutil.make_archive(backup_base, 'zip', str(dst_brain))
                print(f"Backed up existing brain to {backup_base}.zip")
            shutil.copytree(src_brain, dst_brain, dirs_exist_ok=True)
            print(f"Imported brain directory for {conversation_id}")
            
        # 2. Restore DB
        src_db = uuid_dir / "conversations" / f"{conversation_id}.db"
        if src_db.exists():
            dst_db = agy_root / "conversations" / f"{conversation_id}.db"
            dst_db.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_db, dst_db)
            print(f"Imported db for {conversation_id}")
            
        # 3. Restore summary
        src_summary = uuid_dir / "summary.json"
        if src_summary.exists():
            try:
                with open(src_summary, 'r', encoding='utf-8') as f:
                    summary_data = json.load(f)
                summary_db = agy_root / "conversation_summaries.db"
                if summary_db.exists():
                    conn = sqlite3.connect(str(summary_db))
                    c = conn.cursor()
                    columns = ', '.join(summary_data.keys())
                    placeholders = ', '.join(['?' for _ in summary_data])
                    values = tuple(summary_data.values())
                    c.execute(f"REPLACE INTO conversation_summaries ({columns}) VALUES ({placeholders})", values)
                    conn.commit()
                    conn.close()
                    print(f"Imported summary for {conversation_id}")
            except Exception as e:
                print(f"Error importing summary for {conversation_id}: {e}")
                
        imported_count += 1
        
    print(f"Finished! Imported {imported_count} conversations from project sync dir.")

def main():
    parser = argparse.ArgumentParser(description="Export raw conversation log.")
    parser.add_argument('--app-data-dir', required=True, help="Path to Antigravity app data dir")
    parser.add_argument('--conversation-id', required=False, help="Current conversation ID")
    parser.add_argument('--output-dir', required=False, help="Directory to save the exported log")
    parser.add_argument('--all-for-project', required=False, help="Path to project to export all related conversations")
    parser.add_argument('--import-for-project', required=False, help="Path to project to import all synced conversations")
    args = parser.parse_args()

    if args.import_for_project:
        project_path = os.path.abspath(args.import_for_project)
        import_brains(args.app_data_dir, project_path)
        return

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

    if args.all_for_project:
        project_path = os.path.abspath(args.all_for_project)
        # Use lower() for comparison but keep original path for copying
        project_path_lower = project_path.lower()
        brain_dir = os.path.join(args.app_data_dir, "brain")
        print(f"Scanning all conversations for project: {project_path}")
        
        exported_count = 0
        for conv_id in os.listdir(brain_dir):
            conv_dir = os.path.join(brain_dir, conv_id)
            if not os.path.isdir(conv_dir): continue
            
            transcript_path = os.path.join(conv_dir, ".system_generated", "logs", "transcript.jsonl")
            if not os.path.exists(transcript_path): continue
            
            # Read first few lines to see if project path is in <user_information>
            is_related = False
            try:
                with open(transcript_path, 'r', encoding='utf-8') as f:
                    for _ in range(50):
                        line = f.readline()
                        if not line: break
                        if project_path_lower in line.lower() or os.path.basename(project_path_lower).lower() in line.lower():
                            is_related = True
                            break
            except Exception:
                pass
                
            if is_related:
                if export_conversation(args.app_data_dir, conv_id, args.output_dir):
                    exported_count += 1
                    # Also backup raw brain state for 'all' mode
                    backup_brain_state(args.app_data_dir, conv_id, project_path)
                    
        print(f"Finished! Exported {exported_count} related conversations.")
    
    elif args.conversation_id and args.output_dir:
        export_conversation(args.app_data_dir, args.conversation_id, args.output_dir)
    else:
        print("Error: Must provide either --conversation-id, --all-for-project, or --import-for-project")

if __name__ == "__main__":
    main()
