import argparse
import json
import os
import datetime
import re
import sqlite3

def decode_varint(data, offset):
    result = 0
    shift = 0
    while offset < len(data):
        b = data[offset]
        result |= (b & 0x7F) << shift
        offset += 1
        if not (b & 0x80):
            return result, offset
        shift += 7
    raise Exception("Unterminated varint")

def parse_protobuf(data, strings_out):
    offset = 0
    while offset < len(data):
        try:
            key, offset = decode_varint(data, offset)
            wire_type = key & 0x7
            if wire_type == 0:
                _, offset = decode_varint(data, offset)
            elif wire_type == 1:
                offset += 8
            elif wire_type == 5:
                offset += 4
            elif wire_type == 2:
                length, offset = decode_varint(data, offset)
                if length > len(data) - offset:
                    break
                payload = data[offset:offset+length]
                offset += length
                try:
                    s = payload.decode('utf-8')
                    if len(s) > 10:
                        printable_ratio = sum(1 for c in s if c.isprintable() or c in '\n\r\t') / len(s)
                        if printable_ratio > 0.95:
                            strings_out.append(s)
                except UnicodeDecodeError:
                    pass
                if len(payload) > 0:
                    try:
                        parse_protobuf(payload, strings_out)
                    except Exception:
                        pass
            else:
                break
        except Exception:
            break

def is_garbage(text):
    if text.startswith('{"'): return True
    if text.startswith('agy --'): return True
    if len(text) < 10: return True
    return False

def write_markdown_logs(conversation_id, output_dir, daily_logs):
    if output_dir is None:
        output_dir = os.getcwd()
    for date_str, messages in daily_logs.items():
        if not messages: continue
        
        output_path = os.path.join(output_dir, f"explore_log_{date_str}.md")
        
        markdown_content = f"<!-- CONVERSATION_START: {conversation_id}_{date_str} -->\n"
        markdown_content += f"## 對話與探索紀錄 (Conversation ID: `{conversation_id}` - {date_str})\n"
        markdown_content += f"更新時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        markdown_content += "---\n\n"
        
        for msg in messages:
            markdown_content += msg
            
        markdown_content += f"<!-- CONVERSATION_END: {conversation_id}_{date_str} -->\n\n"
        
        existing_content = ""
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as ef:
                existing_content = ef.read()
                
            pattern = rf"<!-- CONVERSATION_START: {conversation_id}_{date_str} -->.*?<!-- CONVERSATION_END: {conversation_id}_{date_str} -->\n*"
            existing_content = re.sub(pattern, "", existing_content, flags=re.DOTALL)

        with open(output_path, 'w', encoding='utf-8') as out:
            if existing_content.strip():
                out.write(existing_content.rstrip() + "\n\n")
            out.write(markdown_content)
            
        print(f"Log exported successfully: {conversation_id} -> {output_path}")

def clean_system_text(text):
    text = re.sub(r'<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>', '', text, flags=re.DOTALL)
    text = re.sub(r'<EPHEMERAL_MESSAGE>.*?</EPHEMERAL_MESSAGE>', '', text, flags=re.DOTALL)
    text = re.sub(r'<SKILL>.*?</SKILL>', '', text, flags=re.DOTALL)
    text = re.sub(r'<SYSTEM_MESSAGE>.*?</SYSTEM_MESSAGE>', '', text, flags=re.DOTALL)
    text = re.sub(r'The following is an <EPHEMERAL_MESSAGE>.*?act accordingly\.', '', text, flags=re.DOTALL)
    
    text = re.sub(r'\*\*[^*]+\*\*\n+(?:I\'m|I\'ve|I am|I will) .*?(?=\n\n|\Z)', '', text, flags=re.DOTALL)
    text = re.sub(r'(?mi)^[ \t]*bot[^\n]*', '', text)
    text = re.sub(r'(?m)^[ \t]*\*\*[^\n]*', '', text)
    text = re.sub(r'(?m)^[ \t]*\$[^\n]*', '', text)
    text = re.sub(r'[^\n]*(?:I\'m|I\'ve|I am|I will) [^\n]*', '', text)
    text = re.sub(r'[^\n]*explicitly invoked[^\n]*', '', text)
    text = re.sub(r'[^\n]*CRITICAL INSTRUCTION[^\n]*', '', text)
    text = re.sub(r'[^\n]*file:///[^\n]*', '', text)
    text = re.sub(r'The user is currently editing the file.*?(?=\n|\Z)', '', text)
    text = re.sub(r'(?i)[^\n]*All artifacts complete[^\n]*', '', text)
    
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def clean_user_text(text):
    req_match = re.search(r'<USER_REQUEST>(.*?)</USER_REQUEST>', text, re.DOTALL)
    if req_match:
        return req_match.group(1).strip()
    return clean_system_text(text)

def extract_conversation_from_db(app_data_dir, conversation_id, output_dir):
    try:
        db_path = os.path.join(app_data_dir, "conversations", f"{conversation_id}.db")
        if not os.path.exists(db_path):
            return False
            
        daily_logs = {}
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT idx, step_type, step_payload FROM steps WHERE step_type IN (14, 15) ORDER BY idx DESC")
        
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        summary_db = os.path.join(app_data_dir, "conversation_summaries.db")
        if os.path.exists(summary_db):
            try:
                sc = sqlite3.connect(summary_db).cursor()
                sc.execute("SELECT last_modified_time FROM conversation_summaries WHERE conversation_id=?", (conversation_id,))
                row = sc.fetchone()
                if row and row[0]:
                    dt = datetime.datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%SZ")
                    dt_local = dt + datetime.timedelta(hours=8)
                    date_str = dt_local.strftime("%Y-%m-%d")
                sc.connection.close()
            except:
                pass
                
        daily_logs[date_str] = []
        
        for idx, step_type, payload in c.fetchall():
            if not payload: continue
            
            strings = []
            parse_protobuf(payload, strings)
            valid_strings = [s for s in strings if not is_garbage(s)]
            
            if not valid_strings: continue
            
            longest_string = max(valid_strings, key=len)
            text = longest_string.strip()
            
            if step_type == 14:
                text = clean_user_text(text)
                if not text: continue
                daily_logs[date_str].append(f"### 👤\n\n{text}\n\n---\n\n")
            elif step_type == 15:
                text = clean_system_text(text)
                if not text: continue
                daily_logs[date_str].append(f"### 🤖\n\n{text}\n\n---\n\n")
                
        if not daily_logs[date_str]:
            return False
            
        write_markdown_logs(conversation_id, output_dir, daily_logs)
        return True
    except Exception as e:
        print(f"Failed to export from DB {conversation_id}: {e}")
        return False

def export_conversation(app_data_dir, conversation_id, output_dir):
    logs_dir = os.path.join(app_data_dir, "brain", conversation_id, ".system_generated", "logs")
    transcript_path = os.path.join(logs_dir, "transcript_full.jsonl")
    
    if not os.path.exists(transcript_path):
        # Fallback to truncated transcript if full one is not available
        transcript_path = os.path.join(logs_dir, "transcript.jsonl")
        
    if not os.path.exists(transcript_path) or os.path.getsize(transcript_path) == 0:
        print(f"WARNING: Transcript for {conversation_id} is missing or 0 bytes. Using SQLite DB fallback.")
        return extract_conversation_from_db(app_data_dir, conversation_id, output_dir)

    try:
        daily_logs = {}
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                try:
                    step = json.loads(line)
                    created_at = step.get('created_at', '')
                    time_str = ""
                    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
                    
                    if created_at:
                        try:
                            dt = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                            dt_local = dt + datetime.timedelta(hours=8)
                            time_str = f" [{dt_local.strftime('%Y-%m-%d %H:%M:%S')}]"
                            date_str = dt_local.strftime("%Y-%m-%d")
                        except:
                            time_str = f" [{created_at}]"

                    if date_str not in daily_logs:
                        daily_logs[date_str] = []

                    if step.get('type') == 'USER_INPUT':
                        content = step.get('content', '')
                        content = clean_user_text(content)
                            
                        if content:
                            daily_logs[date_str].append(f"### 👤{time_str}\n\n" + content + "\n\n---\n\n")
                            
                    elif step.get('type') == 'PLANNER_RESPONSE':
                        content = step.get('content', '')
                        content = clean_system_text(content)
                        if content:
                            daily_logs[date_str].append(f"### 🤖{time_str}\n\n" + content + "\n\n---\n\n")
                            
                except json.JSONDecodeError:
                    pass

        for date_str in daily_logs:
            daily_logs[date_str].reverse()
        write_markdown_logs(conversation_id, output_dir, daily_logs)
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
        
    backups = []
    for uuid_dir in sync_dir.iterdir():
        if not uuid_dir.is_dir(): continue
        
        conversation_id = uuid_dir.name
        summary_path = uuid_dir / "summary.json"
        
        title = ""
        preview = ""
        last_modified = ""
        raw_ts = ""
        
        if summary_path.exists():
            try:
                with open(summary_path, 'r', encoding='utf-8') as f:
                    summary_data = json.load(f)
                    title = summary_data.get('title', '')
                    preview = summary_data.get('preview', '')
                    ts = summary_data.get('last_modified_time', '')
                    if ts:
                        raw_ts = ts
                        try:
                            import datetime
                            dt = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
                            dt_local = dt + datetime.timedelta(hours=8)
                            last_modified = dt_local.strftime('%Y-%m-%d %H:%M:%S')
                        except:
                            last_modified = ts
            except:
                pass
                
        display_name = title if title else preview
        if not display_name:
            display_name = "Untitled Conversation"
            
        # Extract last user and AI messages
        user_msg = ""
        ai_msg = ""
        paths_to_check = [
            uuid_dir / ".system_generated" / "logs" / "transcript_full.jsonl",
            uuid_dir / "brain" / ".system_generated" / "logs" / "transcript_full.jsonl",
            uuid_dir / ".system_generated" / "logs" / "transcript.jsonl",
            uuid_dir / "brain" / ".system_generated" / "logs" / "transcript.jsonl"
        ]
        
        transcript_path = None
        for p in paths_to_check:
            if p.exists() and p.stat().st_size > 0:
                transcript_path = p
                break
                
        if transcript_path:
            try:
                with open(transcript_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if not line.strip(): continue
                        try:
                            step = json.loads(line)
                            if not raw_ts and step.get('created_at'):
                                raw_ts = step.get('created_at')
                                try:
                                    import datetime
                                    dt = datetime.datetime.strptime(raw_ts, "%Y-%m-%dT%H:%M:%SZ")
                                    dt_local = dt + datetime.timedelta(hours=8)
                                    last_modified = dt_local.strftime('%Y-%m-%d %H:%M:%S')
                                except:
                                    last_modified = raw_ts

                            step_type = step.get('type', '')
                            if step_type == 'USER_INPUT':
                                user_msg = step.get('content', '')
                            elif step_type in ('PLANNER_RESPONSE', 'MODEL_RESPONSE'):
                                content = step.get('content', '')
                                if content: ai_msg = content
                        except:
                            pass
            except:
                pass
                
        if not raw_ts or not last_modified:
            try:
                import datetime
                mtime = uuid_dir.stat().st_mtime
                dt_local = datetime.datetime.fromtimestamp(mtime)
                raw_ts = dt_local.strftime("%Y-%m-%dT%H:%M:%SZ")
                last_modified = dt_local.strftime('%Y-%m-%d %H:%M:%S')
            except:
                raw_ts = "1970-01-01T00:00:00Z"
                last_modified = "Unknown Date"
                
        if user_msg:
            user_msg = user_msg.replace('\\n', ' ').strip()
            if len(user_msg) > 50: user_msg = user_msg[:47] + "..."
        if ai_msg:
            ai_msg = ai_msg.replace('\\n', ' ').strip()
            if len(ai_msg) > 50: ai_msg = ai_msg[:47] + "..."
            
        backups.append({
            'id': conversation_id,
            'name': display_name,
            'local_time': last_modified,
            'raw_ts': raw_ts,
            'user': user_msg,
            'ai': ai_msg
        })
        
    # Sort backups descending by raw timestamp
    backups.sort(key=lambda x: x['raw_ts'], reverse=True)
    
    print(f"\\nBacked up conversations for {project_path}:")
    print("=" * 80)
    for b in backups:
        print(f"ID: {b['id']}")
        print(f"Name/Preview: {b['name']}")
        if b['local_time']:
            print(f"Last Modified: {b['local_time']}")
        if b['user']:
            print(f"User: {b['user']}")
        if b['ai']:
            print(f"AI:   {b['ai']}")
        print("-" * 80)
        
    print(f"Total {len(backups)} backups found.\\n")

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
        print("\n" + "="*80)
        print("IMPORT COMPLETE! Listing available backups so you can verify and resume:")
        print("="*80)
        list_backups(project_path)
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
        
        # Trigger Viewer Generation
        import subprocess
        from pathlib import Path
        viewer_script = Path(__file__).resolve().parent / "generate_viewer.py"
        if viewer_script.exists():
            subprocess.run([sys.executable, str(viewer_script)])
    
    elif args.conversation_id and args.output_dir:
        export_conversation(args.app_data_dir, args.conversation_id, args.output_dir)
        
        # Trigger Viewer Generation
        import subprocess
        import sys
        from pathlib import Path
        viewer_script = Path(__file__).resolve().parent / "generate_viewer.py"
        if viewer_script.exists():
            subprocess.run([sys.executable, str(viewer_script)])
            
    else:
        print("Error: Must provide either --conversation-id, --all-for-project, or --import-for-project")

if __name__ == "__main__":
    main()
