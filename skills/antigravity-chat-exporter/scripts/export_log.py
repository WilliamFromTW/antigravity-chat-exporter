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

def set_conversation_title(app_data_dir, conversation_id, title):
    try:
        summary_db = os.path.join(app_data_dir, "conversation_summaries.db")
        if os.path.exists(summary_db):
            conn = sqlite3.connect(summary_db)
            c = conn.cursor()
            
            c.execute("SELECT preview FROM conversation_summaries WHERE conversation_id=?", (conversation_id,))
            row = c.fetchone()
            
            if row and row[0]:
                preview = row[0]
                suffix = f"({title})"
                if suffix not in preview:
                    new_preview = f"{preview} {suffix}"
                    c.execute("UPDATE conversation_summaries SET title=?, preview=? WHERE conversation_id=?", (title, new_preview, conversation_id))
                else:
                    c.execute("UPDATE conversation_summaries SET title=? WHERE conversation_id=?", (title, conversation_id))
            else:
                c.execute("UPDATE conversation_summaries SET title=? WHERE conversation_id=?", (title, conversation_id))
                
            conn.commit()
            conn.close()
            print(f"Set title and updated preview for {conversation_id} with '{title}'")
    except Exception as e:
        print(f"Error setting title for {conversation_id}: {e}")

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
                
                # Update workspace_uris to include the new machine's project path
                project_uri = Path(project_path).as_uri()
                existing_uris = summary_data.get('workspace_uris', '')
                
                uris_list = []
                if existing_uris:
                    try:
                        parsed = json.loads(existing_uris)
                        if isinstance(parsed, list):
                            uris_list = parsed
                        else:
                            uris_list = [str(parsed)]
                    except json.JSONDecodeError:
                        uris_list = [existing_uris]
                        
                if not any(project_uri.lower() == u.lower() for u in uris_list):
                    uris_list.insert(0, project_uri)
                    
                summary_data['workspace_uris'] = json.dumps(uris_list)

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

def list_backups(project_path):
    sync_dir = Path(project_path) / ".antigravity_sync" / "brains"
    if not sync_dir.exists():
        print(f"No backups found. Sync directory does not exist: {sync_dir}")
        return
        
    print(f"\nBacked up conversations for {project_path}:")
    print("-" * 70)
    count = 0
    for uuid_dir in sync_dir.iterdir():
        if not uuid_dir.is_dir(): continue
        
        conversation_id = uuid_dir.name
        summary_path = uuid_dir / "summary.json"
        
        title = ""
        preview = ""
        last_modified = ""
        
        if summary_path.exists():
            try:
                with open(summary_path, 'r', encoding='utf-8') as f:
                    summary_data = json.load(f)
                    title = summary_data.get('title', '')
                    preview = summary_data.get('preview', '')
                    # try to get readable time
                    ts = summary_data.get('last_modified_time', '')
                    if ts:
                        try:
                            # Usually 2026-07-09T08:07:29Z
                            import datetime
                            dt = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
                            dt_local = dt + datetime.timedelta(hours=8)
                            last_modified = dt_local.strftime('%Y-%m-%d %H:%M')
                        except:
                            last_modified = ts
            except:
                pass
                
        display_name = title if title else preview
        if not display_name:
            display_name = "Untitled Conversation"
            
        print(f"ID: {conversation_id}")
        print(f"Name/Preview: {display_name}")
        if last_modified:
            print(f"Last Modified: {last_modified}")
        print("-" * 70)
        count += 1
        
    print(f"Total {count} backups found.\n")

def main():
    parser = argparse.ArgumentParser(description="Export raw conversation log.")
    parser.add_argument('--app-data-dir', required=False, help="Path to Antigravity app data dir")
    parser.add_argument('--conversation-id', required=False, help="Current conversation ID")
    parser.add_argument('--output-dir', required=False, help="Directory to save the exported log")
    parser.add_argument('--set-title', required=False, help="Set a custom title for the conversation")
    parser.add_argument('--all-for-project', required=False, help="Path to project to export all related conversations")
    parser.add_argument('--import-for-project', required=False, help="Path to project to import all synced conversations")
    parser.add_argument('--list-backups', required=False, help="Path to project to list all backed up conversations")
    args = parser.parse_args()

    if args.list_backups:
        project_path = os.path.abspath(args.list_backups)
        list_backups(project_path)
        return

    if not args.app_data_dir:
        print("Error: --app-data-dir is required for export/import actions.")
        return

    if args.import_for_project:
        project_path = os.path.abspath(args.import_for_project)
        import_brains(args.app_data_dir, project_path)
        return

    target_conv_id = args.conversation_id
    if args.set_title and not target_conv_id:
        summary_db = os.path.join(args.app_data_dir, "conversation_summaries.db")
        if os.path.exists(summary_db):
            try:
                conn = sqlite3.connect(summary_db)
                c = conn.cursor()
                c.execute("SELECT conversation_id FROM conversation_summaries ORDER BY last_modified_time DESC LIMIT 1")
                row = c.fetchone()
                if row:
                    target_conv_id = row[0]
                conn.close()
            except Exception as e:
                print(f"Failed to auto-detect conversation ID for title setting: {e}")

    if args.set_title and target_conv_id:
        set_conversation_title(args.app_data_dir, target_conv_id, args.set_title)

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

    if args.all_for_project:
        project_path = os.path.abspath(args.all_for_project)
        # Use lower() for comparison but keep original path for copying
        project_path_lower = project_path.lower()
        project_uri = Path(project_path).as_uri()
        project_uri_lower = project_uri.lower()
        
        print(f"Scanning all conversations for project: {project_path}")
        
        related_uuids = set()
        
        # Method 1: Query conversation_summaries.db (Fast and reliable, even if jsonl is empty)
        summary_db = os.path.join(args.app_data_dir, "conversation_summaries.db")
        if os.path.exists(summary_db):
            try:
                conn = sqlite3.connect(summary_db)
                c = conn.cursor()
                c.execute("SELECT conversation_id, workspace_uris FROM conversation_summaries")
                for row in c.fetchall():
                    c_id, uris = row[0], row[1]
                    if uris and (project_uri_lower in uris.lower() or project_path_lower in uris.lower()):
                        related_uuids.add(c_id)
                conn.close()
            except Exception as e:
                print(f"Error querying conversation_summaries.db: {e}")
                
        # Method 2: Fallback to scanning brain directory if DB query missed any
        brain_dir = os.path.join(args.app_data_dir, "brain")
        if os.path.exists(brain_dir):
            for conv_id in os.listdir(brain_dir):
                if conv_id in related_uuids: continue
                conv_dir = os.path.join(brain_dir, conv_id)
                if not os.path.isdir(conv_dir): continue
                
                transcript_path = os.path.join(conv_dir, ".system_generated", "logs", "transcript.jsonl")
                if not os.path.exists(transcript_path): continue
                
                try:
                    with open(transcript_path, 'r', encoding='utf-8') as f:
                        for _ in range(50):
                            line = f.readline()
                            if not line: break
                            if project_path_lower in line.lower() or project_uri_lower in line.lower():
                                related_uuids.add(conv_id)
                                break
                except Exception:
                    pass
                    
        exported_md_count = 0
        backed_up_brain_count = 0
        
        for conv_id in related_uuids:
            if args.set_title:
                set_conversation_title(args.app_data_dir, conv_id, args.set_title)

            # 1. Attempt to export MD (might fail if jsonl is missing/empty, which is fine)
            if export_conversation(args.app_data_dir, conv_id, args.output_dir):
                exported_md_count += 1
                
            # 2. ALWAYS backup raw brain state for related UUIDs
            backup_brain_state(args.app_data_dir, conv_id, project_path)
            backed_up_brain_count += 1
            
        print(f"Finished! Exported {exported_md_count} MD logs, backed up {backed_up_brain_count} Brain DBs.")
    
    elif args.conversation_id and args.output_dir:
        export_conversation(args.app_data_dir, args.conversation_id, args.output_dir)
    else:
        print("Error: Must provide either --conversation-id, --all-for-project, or --import-for-project")

if __name__ == "__main__":
    main()
