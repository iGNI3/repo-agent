const vscode = require('vscode');
const path = require('path');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Repo Agent extension is now active');

    // Create Status Bar Item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'repo-agent.startChat';
    statusBarItem.text = '$(robot) Repo Agent';
    statusBarItem.tooltip = 'Click to start Repo Agent Chat';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    let disposable = vscode.commands.registerCommand('repo-agent.startChat', function () {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            vscode.window.showErrorMessage('No workspace folder open');
            return;
        }

        const repoPath = workspaceFolder.uri.fsPath;
        const raPath = path.join(repoPath, 'ra.bat');

        // Check if ra.bat exists
        const fs = require('fs');
        if (!fs.existsSync(raPath)) {
            vscode.window.showErrorMessage(`ra.bat not found at ${raPath}. Please run install.bat first.`);
            return;
        }

        // Find existing terminal or create new
        let terminal = vscode.window.terminals.find(t => t.name === 'Repo Agent Chat');
        if (!terminal) {
            terminal = vscode.window.createTerminal('Repo Agent Chat');
        }
        
        terminal.sendText(`"${raPath}"`);
        terminal.show();
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}