import pytest
from typer.testing import CliRunner
from ai_dev_toolkit.main import app, register_command
from ai_dev_toolkit.commands.base import Command

runner = CliRunner()

def test_version_command():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "AI Dev Toolkit" in result.stdout

def test_start_command():
    result = runner.invoke(app, ["start"])
    assert result.exit_code == 0
    assert "AI Dev Toolkit" in result.stdout
    assert "Welcome to your development assistant!" in result.stdout

def test_register_command():
    # Create a test command
    class TestCommand(Command):
        def __init__(self):
            super().__init__(name="test-cmd", help="Test command")
        
        def execute(self, param: str = None):
            if param is None:
                param = "default"
            print(f"Executed with {param}")
    
    # Register the command
    test_cmd = TestCommand()
    register_command("test-cmd", test_cmd)
    
    # Test the registered command without parameters
    result = runner.invoke(app, ["test-cmd"])
    assert result.exit_code == 0
    assert "Executed with default" in result.stdout
    
    # Test the registered command with parameters
    result = runner.invoke(app, ["test-cmd", "test"])
    assert result.exit_code == 0
    assert "Executed with test" in result.stdout