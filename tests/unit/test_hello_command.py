import pytest
from ai_dev_toolkit.commands.hello import HelloCommand

def test_hello_command_initialization():
    cmd = HelloCommand()
    assert cmd.name == "hello"
    assert cmd.help == "A friendly greeting command"

def test_hello_command_execute_default(capsys):
    cmd = HelloCommand()
    cmd.execute()
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out

def test_hello_command_execute_custom_name(capsys):
    cmd = HelloCommand()
    cmd.execute(name="Test")
    captured = capsys.readouterr()
    assert "Hello, Test!" in captured.out 