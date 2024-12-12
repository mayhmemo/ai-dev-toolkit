import pytest
from ai_dev_toolkit.commands.base import Command

def test_command_initialization():
    cmd = Command(name="test", help="Test command")
    assert cmd.name == "test"
    assert cmd.help == "Test command"

def test_command_execute_not_implemented():
    cmd = Command(name="test", help="Test command")
    with pytest.raises(NotImplementedError):
        cmd.execute()

def test_command_display_info(capsys):
    cmd = Command(name="test", help="Test command")
    cmd.display_info()
    captured = capsys.readouterr()
    assert "test" in captured.out
    assert "Test command" in captured.out 