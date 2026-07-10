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

def main():
    parser = argparse.ArgumentParser(description="Export raw conversation log.")
    parser.add_argument('--app-data-dir', required=True, help="Path to Antigravity app data dir")
    parser.add_argument('--conversation-id', required=False, help="Current conversation ID")
    parser.add_argument('--output-dir', required=True, help="Directory to save the exported log")
    parser.add_argument('--all-for-project', required=False, help="Path to project to export all related conversations")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    if args.all_for_project:
        project_path = os.path.abspath(args.all_for_project).lower()
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
                        if project_path in line.lower() or os.path.basename(project_path).lower() in line.lower():
                            is_related = True
                            break
            except Exception:
                pass
                
            if is_related:
                if export_conversation(args.app_data_dir, conv_id, args.output_dir):
                    exported_count += 1
                    
        print(f"Finished! Exported {exported_count} related conversations.")
    
    elif args.conversation_id:
        export_conversation(args.app_data_dir, args.conversation_id, args.output_dir)
    else:
        print("Error: Must provide either --conversation-id or --all-for-project")

if __name__ == "__main__":
    main()
