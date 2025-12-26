"""
SLASHY MAIL - CHROME INTEGRATION MODULE
Browser automation helpers for Claude Code Chrome integration

Usage with Claude Code:
1. Start Claude Code with Chrome: `claude --chrome`
2. Navigate to https://slashy.com in your browser
3. Run tests with browser automation

This module provides helpers for keyboard shortcut testing
that work with Claude Code's Chrome extension integration.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
import json


class KeyModifier(Enum):
    """Keyboard modifiers for shortcuts"""
    NONE = ""
    CMD = "Cmd"
    CTRL = "Ctrl"
    SHIFT = "Shift"
    ALT = "Alt"
    CMD_SHIFT = "Cmd+Shift"
    CTRL_SHIFT = "Ctrl+Shift"


@dataclass
class KeyboardShortcut:
    """Represents a keyboard shortcut to test"""
    key: str
    modifier: KeyModifier = KeyModifier.NONE
    description: str = ""
    expected_action: str = ""

    @property
    def combo(self) -> str:
        """Get the full key combination string"""
        if self.modifier == KeyModifier.NONE:
            return self.key
        return f"{self.modifier.value}+{self.key}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "modifier": self.modifier.value,
            "combo": self.combo,
            "description": self.description,
            "expected_action": self.expected_action
        }


class SlashyShortcuts:
    """
    Slashy Mail keyboard shortcuts catalog
    Reference: https://slashy.com keyboard shortcuts
    """

    # Composing & Replying
    COMPOSE = KeyboardShortcut("C", KeyModifier.NONE, "Compose mail", "Opens compose window")
    REPLY = KeyboardShortcut("R", KeyModifier.NONE, "Reply", "Opens reply composer")

    # Navigation
    MOVE_DOWN = KeyboardShortcut("J", KeyModifier.NONE, "Move down", "Navigate to next email")
    MOVE_UP = KeyboardShortcut("K", KeyModifier.NONE, "Move up", "Navigate to previous email")
    JUMP_TOP = KeyboardShortcut("Up", KeyModifier.CMD, "Jump to top", "Go to first email")
    JUMP_BOTTOM = KeyboardShortcut("Down", KeyModifier.CMD, "Jump to bottom", "Go to last email")

    # Email Actions
    MARK_DONE = KeyboardShortcut("E", KeyModifier.NONE, "Mark as done", "Move to Done folder")
    MARK_NOT_DONE = KeyboardShortcut("E", KeyModifier.SHIFT, "Mark not done", "Undo mark as done")
    STAR = KeyboardShortcut("S", KeyModifier.NONE, "Star email", "Toggle star")
    TOGGLE_READ = KeyboardShortcut("U", KeyModifier.NONE, "Toggle read/unread", "Toggle read state")
    TRASH = KeyboardShortcut("#", KeyModifier.NONE, "Move to trash", "Delete email")
    SPAM = KeyboardShortcut("!", KeyModifier.NONE, "Mark as spam", "Report as spam")

    # Features
    SET_REMINDER = KeyboardShortcut("H", KeyModifier.NONE, "Set reminder", "Open reminder dialog")
    SEARCH = KeyboardShortcut("/", KeyModifier.NONE, "Search", "Open search bar")

    # Multi-key shortcuts
    CREATE_LABEL = KeyboardShortcut("N+L", KeyModifier.NONE, "Create label", "Open label dialog")
    CREATE_SNIPPET = KeyboardShortcut("N+S", KeyModifier.NONE, "Create snippet", "Open snippet dialog")
    AI_AGENT = KeyboardShortcut("P+A", KeyModifier.NONE, "AI agent chat", "Open AI assistant")

    # Selection
    SELECT_ALL_FROM = KeyboardShortcut("A", KeyModifier.CMD, "Select all from here", "Select visible emails")
    SELECT_ALL = KeyboardShortcut("A", KeyModifier.CMD_SHIFT, "Select all emails", "Select all emails")

    # Interface
    TOGGLE_LEFT_SIDEBAR = KeyboardShortcut("B", KeyModifier.CMD, "Toggle left sidebar", "Show/hide left panel")
    TOGGLE_RIGHT_SIDEBAR = KeyboardShortcut(".", KeyModifier.CMD, "Toggle right sidebar", "Show/hide right panel")

    # Label Cycling
    CYCLE_FORWARD = KeyboardShortcut("Tab", KeyModifier.NONE, "Cycle labels forward", "Next label tab")
    CYCLE_BACKWARD = KeyboardShortcut("Tab", KeyModifier.SHIFT, "Cycle labels backward", "Previous label tab")

    # Inbox Navigation
    PREV_INBOX = KeyboardShortcut("[", KeyModifier.NONE, "Previous inbox", "Switch to previous inbox")
    NEXT_INBOX = KeyboardShortcut("]", KeyModifier.NONE, "Next inbox", "Switch to next inbox")

    # Email Control
    OPEN_EMAIL = KeyboardShortcut("Enter", KeyModifier.NONE, "Open email", "Open focused email")
    SET_LABEL = KeyboardShortcut("L", KeyModifier.NONE, "Set label", "Open label selector")
    BLOCK_SENDER = KeyboardShortcut("U", KeyModifier.CMD, "Block sender", "Block email sender")

    @classmethod
    def get_all(cls) -> List[KeyboardShortcut]:
        """Get all defined shortcuts"""
        shortcuts = []
        for name in dir(cls):
            attr = getattr(cls, name)
            if isinstance(attr, KeyboardShortcut):
                shortcuts.append(attr)
        return shortcuts

    @classmethod
    def to_json(cls) -> str:
        """Export all shortcuts as JSON"""
        return json.dumps([s.to_dict() for s in cls.get_all()], indent=2)


class ChromeTestInstructions:
    """
    Instructions for testing with Claude Code Chrome integration
    """

    @staticmethod
    def get_setup_instructions() -> str:
        return """
╔══════════════════════════════════════════════════════════════════╗
║           SLASHY MAIL CHROME INTEGRATION SETUP                   ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  OPTION 1: Built-in Chrome Integration (Recommended)            ║
║  ────────────────────────────────────────────────────            ║
║  1. Install Claude in Chrome extension (v1.0.36+)               ║
║  2. Start Claude Code with: claude --chrome                     ║
║  3. Navigate to https://slashy.com in Chrome                    ║
║  4. Ask Claude to test keyboard shortcuts                       ║
║                                                                  ║
║  OPTION 2: MCP Chrome DevTools                                  ║
║  ────────────────────────────────────────────────────            ║
║  1. Run: claude mcp add chrome-devtools \\                       ║
║          npx chrome-devtools-mcp@latest                         ║
║  2. Launch Chrome with debugging:                               ║
║     google-chrome --remote-debugging-port=9222                  ║
║  3. Navigate to https://slashy.com                              ║
║  4. Run tests via Claude Code                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

    @staticmethod
    def get_test_prompts() -> List[str]:
        """Get example prompts for Claude Code Chrome testing"""
        return [
            "Navigate to slashy.com and log in",
            "Press 'C' and verify the compose window opens",
            "Test the J/K navigation shortcuts on the inbox",
            "Press Cmd+B to toggle the left sidebar",
            "Test all keyboard shortcuts and report which ones work",
            "Take a screenshot of the current page",
            "Check the browser console for any errors",
        ]


def print_setup():
    """Print setup instructions"""
    print(ChromeTestInstructions.get_setup_instructions())
    print("\nExample test prompts for Claude Code:")
    print("-" * 50)
    for i, prompt in enumerate(ChromeTestInstructions.get_test_prompts(), 1):
        print(f"  {i}. \"{prompt}\"")
    print()


def print_shortcuts():
    """Print all shortcuts in a formatted table"""
    shortcuts = SlashyShortcuts.get_all()
    print("\n" + "=" * 70)
    print("SLASHY MAIL KEYBOARD SHORTCUTS")
    print("=" * 70)
    print(f"{'Shortcut':<20} {'Description':<25} {'Action'}")
    print("-" * 70)
    for s in shortcuts:
        print(f"{s.combo:<20} {s.description:<25} {s.expected_action}")
    print("=" * 70)
    print(f"Total shortcuts: {len(shortcuts)}")
    print()


if __name__ == "__main__":
    print_setup()
    print_shortcuts()
