from agents.planner_agent import create_plan
from agents.coder_agent import implement
from agents.reviewer_agent import review_code
from core.file_search import search_files
import re
import os
from core.file_editor import write_file


def run_agents(vector_store, task):
    print("Planning...")
    # Get repository structure
    file_list = "\n".join(vector_store.metadata.get(i, {}).get("path", "") for i in range(vector_store.index.ntotal))

    plan = create_plan(task, file_list)
    print(f"\nPLAN:\n{plan}")

    files = search_files(vector_store, task)
    context = "\n".join(f["content"][:2000] for f in files)

    print("Generating code...")
    code_response = implement(plan, context)

    print("Reviewing code...")
    reviewed_code = review_code(plan, code_response)

    # Parse file changes
    # Expected format: FILE: path/to/file\n```python\ncontent\n```
    file_blocks = re.findall(r"FILE:\s*(.*?)\n```(?:\w+)?\n(.*?)\n```", reviewed_code, re.DOTALL)

    if not file_blocks:
        print("No file changes detected in the agent response.")
        return reviewed_code

    for file_path, new_content in file_blocks:
        file_path = file_path.strip()
        print(f"\n--- Proposed changes for: {file_path} ---")
        # Simple preview (first 10 lines)
        preview = "\n".join(new_content.splitlines()[:10])
        print(preview)
        if len(new_content.splitlines()) > 10:
            print("...")

        confirm = input(f"\nApply these changes to {file_path}? (y/n): ").strip().lower()
        if confirm == 'y':
            # Ensure path is absolute if it's not
            if not os.path.isabs(file_path):
                # We assume file_path is relative to the repo root which we don't have here easily
                # but let's try to handle it or just write it as is.
                pass
            write_file(file_path, new_content)
            print(f"Successfully updated {file_path}")
        else:
            print(f"Skipped {file_path}")

    return "All approved changes applied."