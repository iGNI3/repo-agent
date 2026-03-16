import os
import re

def grep(pattern, directory='.', recursive=True):
    """
    Search for a pattern in files within a directory.
    """
    results = []
    try:
        if recursive:
            for root, dirs, files in os.walk(directory):
                # Ignore common folders
                if any(x in root for x in [".git", "env", "__pycache__", "node_modules"]):
                    continue
                for file in files:
                    results.extend(_search_in_file(os.path.join(root, file), pattern))
        else:
            for file in os.listdir(directory):
                path = os.path.join(directory, file)
                if os.path.isfile(path):
                    results.extend(_search_in_file(path, pattern))
    except Exception as e:
        return f"Error during grep: {e}"
    
    return "\n".join(results) if results else "No matches found."

def _search_in_file(path, pattern):
    matches = []
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_no, line in enumerate(f, 1):
                if re.search(pattern, line):
                    matches.append(f"{path}:{line_no}: {line.strip()}")
    except:
        pass
    return matches
