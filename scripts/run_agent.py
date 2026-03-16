import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from workflows.autonomous_dev_loop import run_loop


def main():

    if len(sys.argv) < 3:
        print("Usage:")
        print("python scripts/run_agent.py <repo_path> <task>")
        return

    repo_path = sys.argv[1]
    task = sys.argv[2]

    print("Repo:", repo_path)
    print("Task:", task)

    run_loop(repo_path, task)


if __name__ == "__main__":
    main()