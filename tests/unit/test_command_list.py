import pytest
from ai_dev_toolkit.command_list import load_commands
from ai_dev_toolkit.commands.hello import HelloCommand
from ai_dev_toolkit.commands.terminal_builder import TerminalBuilderCommand

def test_load_commands():
    commands = load_commands()
    assert isinstance(commands, dict)
    assert "hello" in commands
    assert "cli-command" in commands
    assert isinstance(commands["hello"], HelloCommand)
    assert isinstance(commands["cli-command"], TerminalBuilderCommand) 