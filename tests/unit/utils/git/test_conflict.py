import subprocess
from unittest.mock import patch, mock_open, MagicMock
from ai_dev_toolkit.utils.git.conflict import get_conflicts, resolve_conflict, abort_merge


class MockFileWithWriteFailure:
    def __init__(self, content):
        self.content = content
        self.write_called = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def read(self):
        return self.content

    def write(self, content):
        self.write_called = True
        raise IOError("Write failed")


@patch("subprocess.run")
def test_get_conflicts_returns_list_of_files_with_merge_conflicts(mock_run):
    mock_run.return_value.stdout = "file1.txt\nfile2.txt\n"
    mock_run.return_value.returncode = 0

    conflicts = get_conflicts()
    assert conflicts == ["file1.txt", "file2.txt"]
    mock_run.assert_called_once_with(
        ["git", "diff", "--name-only", "--diff-filter=U"],
        capture_output=True,
        text=True,
        check=True,
    )


@patch("subprocess.run")
def test_get_conflicts_returns_empty_list_when_git_command_fails(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "git")
    assert get_conflicts() == []


@patch("subprocess.run")
def test_resolve_conflict_keeps_our_changes_and_stages_file(mock_run):
    conflict_content = "before\n<<<<<<< HEAD\nour changes\n=======\ntheir changes\n>>>>>>> branch\nafter"

    mock_file = mock_open(read_data=conflict_content)
    with patch("builtins.open", mock_file):
        assert resolve_conflict("file.txt", "ours") is True

        # Check if the file was written with correct content
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        assert written_content == "before\nour changes\nafter"

        # Check if git add was called
        mock_run.assert_called_once_with(["git", "add", "file.txt"], check=True)


@patch("subprocess.run")
def test_resolve_conflict_keeps_their_changes_and_stages_file(mock_run):
    conflict_content = "before\n<<<<<<< HEAD\nour changes\n=======\ntheir changes\n>>>>>>> branch\nafter"

    mock_file = mock_open(read_data=conflict_content)
    with patch("builtins.open", mock_file):
        assert resolve_conflict("file.txt", "theirs") is True

        # Check if the file was written with correct content
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        assert written_content == "before\ntheir changes\nafter"

        # Check if git add was called
        mock_run.assert_called_once_with(["git", "add", "file.txt"], check=True)


@patch("subprocess.run")
def test_resolve_conflict_with_multiple_conflicts(mock_run):
    conflict_content = (
        "before\n"
        "<<<<<<< HEAD\nour first\n=======\ntheir first\n>>>>>>> branch\n"
        "middle\n"
        "<<<<<<< HEAD\nour second\n=======\ntheir second\n>>>>>>> branch\n"
        "after"
    )

    mock_file = mock_open(read_data=conflict_content)
    with patch("builtins.open", mock_file):
        assert resolve_conflict("file.txt", "ours") is True

        # Check if the file was written with correct content
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        expected_content = "before\nour first\nmiddle\nour second\nafter"
        assert written_content == expected_content, f"Expected:\n{expected_content}\nGot:\n{written_content}"

        # Check if git add was called
        mock_run.assert_called_once_with(["git", "add", "file.txt"], check=True)


def test_resolve_conflict_returns_false_for_invalid_resolution_strategy():
    mock_file = mock_open(read_data="some content")
    with patch("builtins.open", mock_file):
        assert resolve_conflict("file.txt", "invalid") is False


def test_resolve_conflict_returns_false_when_no_conflicts_found():
    mock_file = mock_open(read_data="no conflicts here")
    with patch("builtins.open", mock_file):
        assert resolve_conflict("file.txt", "ours") is False


@patch("subprocess.run")
def test_resolve_conflict_returns_false_when_file_operations_fail(mock_run):
    mock_file = mock_open()
    mock_file.side_effect = IOError()
    with patch("builtins.open", mock_file):
        assert resolve_conflict("file.txt", "ours") is False


@patch("subprocess.run")
def test_resolve_conflict_git_command_fails(mock_run):
    conflict_content = "before\n<<<<<<< HEAD\nour changes\n=======\ntheir changes\n>>>>>>> branch\nafter"
    mock_run.side_effect = subprocess.CalledProcessError(1, "git")
    
    mock_file = mock_open(read_data=conflict_content)
    with patch("builtins.open", mock_file):
        assert resolve_conflict("file.txt", "ours") is False


@patch("subprocess.run")
def test_resolve_conflict_write_fails(mock_run):
    conflict_content = "before\n<<<<<<< HEAD\nour changes\n=======\ntheir changes\n>>>>>>> branch\nafter"
    
    # Create a mock file object that succeeds on read but fails on write
    mock_file = mock_open(read_data=conflict_content)
    mock_file.return_value.__enter__.return_value.write.side_effect = IOError()
    
    with patch("builtins.open", mock_file):
        assert resolve_conflict("file.txt", "ours") is False


@patch("subprocess.run")
def test_resolve_conflict_read_fails(mock_run):
    mock_file = MagicMock()
    mock_file_context = MagicMock()
    mock_file_context.__enter__.return_value.read.side_effect = IOError()
    mock_file.return_value = mock_file_context
    
    with patch("builtins.open", mock_file):
        assert resolve_conflict("file.txt", "ours") is False


@patch("subprocess.run")
def test_abort_merge_cancels_current_merge_operation(mock_run):
    mock_run.return_value.returncode = 0
    assert abort_merge() is True
    mock_run.assert_called_once_with(["git", "merge", "--abort"], check=True)


@patch("subprocess.run")
def test_abort_merge_returns_false_when_git_command_fails(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "git")
    assert abort_merge() is False
