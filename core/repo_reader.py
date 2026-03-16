import os

IGNORE_DIRS = {".git", "node_modules", "env", ".venv", "__pycache__", ".pytest_cache"}
EXTENSIONS = (".py", ".js", ".ts", ".json", ".md")

def read_repo(path):
    repo = {}
    for root, dirs, files in os.walk(path):
        # Prune ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for f in files:
            if f.endswith(EXTENSIONS):
                p = os.path.join(root, f)
                with open(p, "r", errors="ignore") as file:
                    repo[p] = file.read()

    return repo