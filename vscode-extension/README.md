# Repo Agent VS Code Extension

This extension integrates Repo Agent into your VS Code workflow, providing a "Claude Code"-like autonomous development experience.

## Features

- **Status Bar Item**: Quick-access button "$(robot) Repo Agent" in the bottom right.
- **Dedicated Terminal**: Launches a persistent "Repo Agent Chat" terminal.
- **Global CLI Integration**: Uses the reliable `ra.bat` environment.

## Installation

1. Ensure you have run `.\install.bat` in the project root to set up the environment and `ra.bat`.
2. Open the `vscode-extension` folder in VS Code.
3. Press **F5** to start the "Extension Development Host".
4. In the new window, open any codebase.
5. Click the **$(robot) Repo Agent** button in the status bar (bottom right).

## Usage

Once the terminal opens:
1. Enter your task (e.g., "Add a unit test for the file editor").
2. Watch Repo Agent autonomously analyze and modify your code!
3. Type `exit` to close the agent loop.

---
Enjoy your autonomous coding partner!