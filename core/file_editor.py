import os
import logging
import subprocess
from pathlib import Path

def validate_path(workspace_root, target_path):
    """
    Ensures the target path is within the workspace root to prevent path traversal.
    """
    abs_root = os.path.abspath(workspace_root)
    abs_target = os.path.abspath(os.path.join(abs_root, target_path))
    
    if not os.path.commonpath([abs_root, abs_target]) == abs_root:
        raise PermissionError(f"Access denied: {target_path} is outside {workspace_root}")
    return abs_target

def write_file(path, content, workspace_root=None):
    """
    Writes content to a file with path validation.
    """
    if workspace_root is None:
        workspace_root = os.getcwd()
        
    try:
        safe_path = validate_path(workspace_root, path)
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        with open(safe_path, "w", encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        logging.error(f"Failed to write file {path}: {e}")
        return False

def read_file(path, workspace_root=None):
    """
    Reads content from a file with path validation.
    """
    if workspace_root is None:
        workspace_root = os.getcwd()
        
    try:
        safe_path = validate_path(workspace_root, path)
        with open(safe_path, "r", encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Failed to read file {path}: {e}")
        return None

def create_snapshot(repo_path, label):
    """
    Creates a git snapshot of the current state.
    """
    try:
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", f"Snapshot: {label}", "--no-verify"], cwd=repo_path, check=True)
        return True
    except Exception as e:
        logging.error(f"Failed to create snapshot: {e}")
        return False

def rollback(repo_path):
    """
    Rolls back to the last committed state.
    """
    try:
        subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=repo_path, check=True)
        subprocess.run(["git", "clean", "-fd"], cwd=repo_path, check=True)
        return True
    except Exception as e:
        logging.error(f"Failed to rollback: {e}")
        return False