import sys
import os

# add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from workflows.autonomous_dev_loop import run_loop

repo = input("Repo path: ").strip('"')

while True:

    task = input("\nInstruction: ")

    if task == "exit":
        break

    run_loop(repo, task)