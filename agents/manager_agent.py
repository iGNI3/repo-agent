from agents.planner_agent import create_plan
from agents.coder_agent import implement
from agents.reviewer_agent import review_code
from core.file_search import search_files
import re
import os
from core.file_editor import write_file


from core.shell_tool import run_command

from core.grep_tool import grep
from core.shell_tool import run_command

def run_agents(vector_store, task, history=None):
    print("Planning...")
    # Get repository structure - CONSTANTLY USE .docs to avoid previous crash
    file_list = "\n".join(doc.get("path", "") for doc in vector_store.docs) if hasattr(vector_store, 'docs') else "No files indexed."

    # Format history for planning context
    history_str = ""
    if history:
        history_str = "\n--- CONVERSATION HISTORY ---\n"
        for turn in history[-5:]: # Last 5 turns
            history_str += f"{turn['role'].upper()}: {turn['content']}\n"
        history_str += "---------------------------\n"

    plan = create_plan(f"{history_str}\nCurrent Task: {task}", file_list)
    print(f"\n[PLAN]\n{plan}\n")

    confirm_plan = input("Do you want to proceed with this plan? (y/n): ").strip().lower()
    if confirm_plan != 'y':
        print("Plan cancelled by user.")
        return "Plan rejected."

    # Multi-stage simulation: We treat the whole plan as a multi-step execution context
    files = search_files(vector_store, task)
    context = "\n".join(f["content"][:2000] for f in files)

    print("Executing plan...")
    response = implement(plan, context)
    
    # Process the result (Commands, Grep, Files)
    return process_response(response, plan, context)

def process_response(response, plan, context):
    reviewed = review_code(plan, response)

    # 1. Handle GREP
    grep_requests = re.findall(r"GREP:\s*(.*?)$", reviewed, re.MULTILINE)
    for pattern in grep_requests:
        pattern = pattern.strip()
        print(f"\n[Agent Grep]: {pattern}")
        results = grep(pattern)
        print(results[:500] + ("..." if len(results) > 500 else ""))
        # In a real multi-stage agent, we'd feed this back. 
        # For now, we continue to file edits.

    # 2. Handle COMMANDS
    commands = re.findall(r"COMMAND:\s*(.*?)$", reviewed, re.MULTILINE)
    for cmd in commands:
        cmd = cmd.strip()
        confirm = input(f"\nExecute command: {cmd}? (y/n): ").strip().lower()
        if confirm == 'y':
            print(run_command(cmd))

    # 3. Handle FILES
    file_blocks = re.findall(r"FILE:\s*(.*?)\n```(?:\w+)?\n(.*?)\n```", reviewed, re.DOTALL)
    if not file_blocks and not commands and not grep_requests:
        print("\nNo definitive actions taken.")
        return reviewed

    for file_path, new_content in file_blocks:
        file_path = file_path.strip()
        print(f"\n--- Proposed changes for: {file_path} ---")
        preview = "\n".join(new_content.splitlines()[:15])
        print(preview)
        if len(new_content.splitlines()) > 15: print("...")

        confirm = input(f"\nApply changes to {file_path}? (y/n): ").strip().lower()
        if confirm == 'y':
            write_file(file_path, new_content)
            print(f"Successfully updated {file_path}")

    return "Plan execution complete."