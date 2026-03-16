import subprocess
import shlex

def run_command(command):
    """
    Runs a shell command and returns the output.
    """
    try:
        args = shlex.split(command)
        result = subprocess.run(
            args,
            shell=False,
            capture_output=True,
            text=True,
            timeout=30
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Error executing command: {e}"

