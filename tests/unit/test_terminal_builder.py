import pytest
from unittest.mock import patch, MagicMock
from ai_dev_toolkit.commands.terminal_builder import TerminalBuilderCommand, CliResultType

def test_terminal_builder_initialization():
    cmd = TerminalBuilderCommand()
    assert cmd.name == "cli-command"
    assert cmd.help == "Build and execute terminal commands using AI"

@patch('ai_dev_toolkit.commands.terminal_builder.Agent')
@patch('ai_dev_toolkit.commands.terminal_builder.Confirm.ask')
@patch('os.system')
def test_terminal_builder_execute_success(mock_system, mock_confirm, mock_agent):
    # Setup mocks
    mock_result = MagicMock()
    mock_result.data = CliResultType(command="echo test")
    mock_agent_instance = MagicMock()
    mock_agent_instance.run_sync.return_value = mock_result
    mock_agent.return_value = mock_agent_instance
    mock_confirm.return_value = True

    # Execute command
    cmd = TerminalBuilderCommand()
    cmd.execute("print hello")

    # Verify
    mock_agent_instance.run_sync.assert_called_once_with("print hello")
    mock_confirm.assert_called_once()
    mock_system.assert_called_once_with("echo test")

@patch('ai_dev_toolkit.commands.terminal_builder.Agent')
@patch('ai_dev_toolkit.commands.terminal_builder.Confirm.ask')
@patch('os.system')
def test_terminal_builder_execute_no_confirm(mock_system, mock_confirm, mock_agent):
    # Setup mocks
    mock_result = MagicMock()
    mock_result.data = CliResultType(command="echo test")
    mock_agent_instance = MagicMock()
    mock_agent_instance.run_sync.return_value = mock_result
    mock_agent.return_value = mock_agent_instance
    mock_confirm.return_value = False

    # Execute command
    cmd = TerminalBuilderCommand()
    cmd.execute("print hello")

    # Verify
    mock_agent_instance.run_sync.assert_called_once_with("print hello")
    mock_confirm.assert_called_once()
    mock_system.assert_not_called()

@patch('ai_dev_toolkit.commands.terminal_builder.Agent')
def test_terminal_builder_execute_error(mock_agent):
    # Setup mock to raise an exception
    mock_agent_instance = MagicMock()
    mock_agent_instance.run_sync.side_effect = Exception("Test error")
    mock_agent.return_value = mock_agent_instance

    # Execute command and verify error handling
    cmd = TerminalBuilderCommand()
    cmd.execute("print hello")  # Should not raise exception 