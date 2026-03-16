import subprocess
import os

def run_command(command):
    """
    Runs a shell command and returns the output.
    """
    try:
        # Use shell=True for Windows compatibility
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Error executing command: {e}"
