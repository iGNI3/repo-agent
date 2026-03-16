import os

# repository settings
MAX_FILE_CONTEXT = 2000
MAX_REPO_CONTEXT = 20000

# embedding settings
TOP_K_FILES = 5

# agent loop settings
MAX_AUTONOMOUS_LOOPS = 5

# test command
TEST_COMMAND = os.getenv("TEST_COMMAND", "pytest")