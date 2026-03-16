from core.repo_indexer import build_index
from agents.manager_agent import run_agents
from core.command_runner import run
from config.settings import MAX_AUTONOMOUS_LOOPS, TEST_COMMAND


def run_loop(repo_path, task, vector_store=None):
    if vector_store is None:
        print("Indexing repository...")
        vector_store = build_index(repo_path)

    current_task = task
    
    for i in range(MAX_AUTONOMOUS_LOOPS):
        print(f"\n===== LOOP {i+1} =====")
        
        result = run_agents(vector_store, current_task)
        print(result)

        print("\nRunning tests...")
        output = run(TEST_COMMAND)
        print(output)

        if "failed" not in output.lower() and "error" not in output.lower():
            print("Task completed successfully!")
            break
        
        print(f"\n[!] Tests failed. Feedback loop {i+1}/{MAX_AUTONOMOUS_LOOPS}")
        current_task = f"Original Task: {task}\n\nPrevious attempt failed with these errors:\n{output}\n\nPlease fix these errors and try again."