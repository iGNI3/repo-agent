import subprocess
import shlex

def run(cmd):
    """
    Safely runs a command using subprocess without shell=True.
    """
    if not cmd:
        return ""
    
    try:
        args = shlex.split(cmd)
        result = subprocess.run(
            args,
            shell=False,
            # Windows needs some special handling for built-ins if not in shell
            # but for git/pytest/python/ls it should be fine.
            capture_output=True,
            text=True
        )
        return f"{result.stdout}\n{result.stderr}"
    except Exception as e:
        return f"Execution error: {e}"