# Slashy Mail Keyboard Shortcut Tests

Automated testing for [Slashy Mail](https://slashy.com) keyboard shortcuts using Claude Code Chrome integration.

## Chrome Integration Setup

### Option 1: Built-in Chrome Integration (Recommended)

1. Install the [Claude in Chrome](https://chromewebstore.google.com/detail/claude/hcjnhccpfbpmkgopcihgggmlgaejiblm) extension (v1.0.36+)
2. Start Claude Code with Chrome integration:
   ```bash
   claude --chrome
   ```
3. Navigate to https://slashy.com in Chrome
4. Ask Claude to test keyboard shortcuts

### Option 2: MCP Chrome DevTools

1. Add the Chrome DevTools MCP server:
   ```bash
   claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
   ```
2. Launch Chrome with remote debugging:
   ```bash
   google-chrome --remote-debugging-port=9222
   ```
3. Navigate to https://slashy.com
4. Run tests via Claude Code

## Running Tests

```bash
# View shortcuts and setup instructions
python chrome_integration.py

# Run the test suite
python slashy_shortcut_tests.py
```

## Example Claude Code Prompts

Once Chrome integration is enabled, you can ask Claude Code to:

- "Navigate to slashy.com and log in"
- "Press 'C' and verify the compose window opens"
- "Test the J/K navigation shortcuts on the inbox"
- "Press Cmd+B to toggle the left sidebar"
- "Test all keyboard shortcuts and report which ones work"

## Files

- `slashy_shortcut_tests.py` - Test suite with recorded results
- `chrome_integration.py` - Chrome integration helpers and shortcut catalog
- `.claude/settings.json` - Claude Code Chrome configuration
