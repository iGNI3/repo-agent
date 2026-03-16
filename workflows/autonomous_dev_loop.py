from core.repo_indexer import build_index
from agents.manager_agent import run_agents
from core.command_runner import run
from config.settings import MAX_AUTONOMOUS_LOOPS, TEST_COMMAND


def run_loop(repo_path, task, vector_store=None, history=None):
    from core.state_manager import StateManager
    state = StateManager()
    
    if vector_store is None:
        print("Indexing repository...")
        vector_store = build_index(repo_path)

    current_task = task
    failure_count = 0
    
    for i in range(MAX_AUTONOMOUS_LOOPS):
        print(f"\n===== LOOP {i+1} =====")
        state.set("status", f"executing_loop_{i+1}")
        
        result = run_agents(vector_store, current_task, history=history)
        if result == "Plan rejected.":
            return "Task cancelled by user."
            
        print(result)

        print("\nRunning tests...")
        output = run(TEST_COMMAND)
        print(output)

        if "failed" not in output.lower() and "error" not in output.lower():
            print("Task completed successfully!")
            state.set("status", "completed")
            return result 
        
        failure_count += 1
        if failure_count >= 3:
            print("\n[!] Circuit Breaker Triggered: Agent failed 3 consecutive attempts.")
            state.set("status", "failed_circuit_breaker")
            return "Task failed: Circuit breaker triggered after 3 failed attempts."

        print(f"\n[!] Tests failed. Feedback loop {i+1}/{MAX_AUTONOMOUS_LOOPS}")
        current_task = f"Original Task: {task}\n\nPrevious attempt failed with these errors:\n{output}\n\nPlease fix these errors and try again."
    
    state.set("status", "failed_max_loops")
    return "Task exceeded maximum loops."