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

    # Index once at startup
    print(f"Indexing repository at {repo_path}...")
    try:
        from core.repo_indexer import build_index
        vector_store = build_index(repo_path)
    except Exception as e:
        print(f"Error during indexing: {e}")
        return

    if args.task:
        print(f"Running task: {args.task}")
        run_loop(repo_path, args.task, vector_store=vector_store)
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
                
                run_loop(repo_path, task, vector_store=vector_store)
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
