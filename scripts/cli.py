import sys
import os
import argparse

# add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from workflows.autonomous_dev_loop import run_loop

def find_repo_root():
    """Simple check for git or a project marker."""
    curr = os.getcwd()
    while curr != os.path.dirname(curr):
        if os.path.isdir(os.path.join(curr, ".git")):
            return curr
        curr = os.path.dirname(curr)
    return os.getcwd()

def main():
    parser = argparse.ArgumentParser(description="Repo-Agent: Claude Code-like CLI")
    parser.add_argument("task", nargs="?", help="Specific task to perform. If omitted, starts interactive mode.")
    parser.add_argument("--repo", default=find_repo_root(), help="Path to the repository (defaults to current dir or git root)")
    
    args = parser.parse_args()
    repo_path = os.path.abspath(args.repo)
    
    # Robust dotenv loading from project root
    from dotenv import load_dotenv
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    load_dotenv(os.path.join(project_root, ".env"), override=True)

    index_cache_path = os.path.join(repo_path, ".repo-agent", "index")
    history_path = os.path.join(repo_path, ".repo-agent", "history.json")
    
    from core.vector_store import VectorStore
    from core.repo_indexer import build_index
    from core.memory_manager import MemoryManager

    memory = MemoryManager(history_path)

    if os.path.exists(index_cache_path + ".index"):
        print(f"Loading cached index for {repo_path}...")
        try:
            vector_store = VectorStore.load(index_cache_path)
        except Exception as e:
            print(f"Failed to load index: {e}. Re-indexing...")
            vector_store = build_index(repo_path)
            vector_store.save(index_cache_path)
    else:
        print(f"Indexing repository at {repo_path}...")
        try:
            vector_store = build_index(repo_path)
            vector_store.save(index_cache_path)
        except Exception as e:
            print(f"Error during indexing: {e}")
            if "401" in str(e):
                print("Tip: Check your OPENROUTER_API_KEY in .env")
            return

    if args.task:
        print(f"Running task: {args.task}")
        memory.add_turn("user", args.task)
        result = run_loop(repo_path, args.task, vector_store=vector_store, history=memory.get_context())
        memory.add_turn("assistant", result)
    else:
        print(f"--- Welcome to Repo-Agent ---")
        print(f"Project root identified as: {repo_path}")
        print("Type 'exit' or use Ctrl+C to quit.")
        
        while True:
            try:
                task = input("\n[ra] > ").strip()
                if not task:
                    continue
                if task.lower() in ("exit", "quit"):
                    break
                
                memory.add_turn("user", task)
                result = run_loop(repo_path, task, vector_store=vector_store, history=memory.get_context())
                memory.add_turn("assistant", result)
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
