@echo off
set REPO_AGENT_DIR=C:\Users\intel\Desktop\repo-agent\
call "%REPO_AGENT_DIR%env\Scripts\activate.bat"
python "%REPO_AGENT_DIR%scripts\cli.py" %*
