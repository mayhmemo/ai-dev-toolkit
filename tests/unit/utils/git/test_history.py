import subprocess
from unittest.mock import patch
from datetime import datetime
import pytest
from ai_dev_toolkit.utils.git.history import get_file_history, blame, find_commit


@pytest.fixture
def git_commit_line():
    """Fixture providing a standard git commit line format."""
    return "hash1|author1|email1@test.com|1609459200|message1"


@pytest.fixture
def blame_commit_info():
    """Fixture providing standard blame commit information."""
    return """abcd1234 1 1 1
author John Doe
author-mail <john@example.com>
author-time 1609459200
summary Initial commit
\tline of code"""


@patch("subprocess.run")
def test_should_return_commit_history_when_file_exists(mock_run, git_commit_line):
    """
    Test that get_file_history returns properly formatted commit history when file exists.
    Verifies all commit fields are correctly parsed and formatted.
    """
    mock_run.return_value.stdout = f"{git_commit_line}\n"
    result = get_file_history("file.txt")
    assert len(result) == 1
    assert result[0]["hash"] == "hash1"
    assert result[0]["author"] == "author1"
    assert result[0]["email"] == "email1@test.com"
    assert result[0]["message"] == "message1"
    assert isinstance(result[0]["date"], datetime)


@pytest.mark.parametrize("output,expected_count", [
    ("hash1|author1|email1@test.com|1609459200|message1\n\n", 1),
    ("hash1|author1|email1@test.com|1609459200|message1\n\nHash2|author2|email2@test.com|1609459200|message2\n\n", 2),
    ("\n\n", 0),
])
@patch("subprocess.run")
def test_should_handle_empty_lines_when_getting_file_history(mock_run, output, expected_count):
    """
    Test that get_file_history properly handles empty lines in git output.
    Verifies that empty lines are ignored and only valid commit lines are processed.
    """
    mock_run.return_value.stdout = output
    result = get_file_history("file.txt")
    assert len(result) == expected_count


@pytest.mark.parametrize("command,function,args", [
    (["git", "log", "--follow", "--pretty=format:%H|%an|%ae|%at|%s", "--", "file.txt"], get_file_history, ["file.txt"]),
    (["git", "blame", "--porcelain", "file.txt"], blame, ["file.txt"]),
    (["git", "log", "--all", "--grep", "test", "--pretty=format:%H|%an|%ae|%at|%s"], find_commit, ["test"]),
])
@patch("subprocess.run")
def test_should_return_empty_list_when_git_command_fails(mock_run, command, function, args):
    """
    Test that all git commands return empty list when the command fails.
    Verifies consistent error handling across different git operations.
    """
    mock_run.side_effect = subprocess.CalledProcessError(1, command)
    assert function(*args) == []


@pytest.mark.parametrize("blame_output,expected_commits", [
    # Complete commit with code
    ("""abcd1234 1 1 1
author John Doe
author-mail <john@example.com>
author-time 1609459200
summary Initial commit
\tline of code""", 1),
    # Multiple complete commits
    ("""abcd1234 1 1 1
author John Doe
author-mail <john@example.com>
author-time 1609459200
summary Initial commit
\tline of code
ef789012 2 2 1
author Jane Smith
author-mail <jane@example.com>
author-time 1609545600
summary Second commit
\tanother line""", 2),
    # Commit without code
    ("""abcd1234 1 1 1
author John Doe
author-mail <john@example.com>
author-time 1609459200
summary Initial commit""", 0),
])
@patch("subprocess.run")
def test_should_handle_different_blame_outputs(mock_run, blame_output, expected_commits):
    """
    Test that blame handles different git blame outputs correctly.
    Verifies proper parsing of commit information and code lines.
    """
    mock_run.return_value.stdout = blame_output
    result = blame("file.txt")
    assert len(result) == expected_commits
    if expected_commits > 0:
        assert all("code" in commit for commit in result)


@patch("subprocess.run")
def test_should_handle_multiple_lines_from_same_commit_when_blaming(mock_run):
    """
    Test that blame correctly handles multiple lines from the same commit.
    Verifies that each line is treated as a separate blame entry even if from same commit.
    """
    blame_output = """abcd1234 1 1 1
author John Doe
author-mail <john@example.com>
author-time 1609459200
summary Initial commit
\tline of code
abcd1234 2 2 1
author John Doe
author-mail <john@example.com>
author-time 1609459200
summary Initial commit
\tline of code 2"""
    mock_run.return_value.stdout = blame_output
    result = blame("file.txt")
    assert len(result) == 2
    assert result[0]["hash"] == result[1]["hash"] == "abcd1234"
    assert result[0]["code"] == "line of code"
    assert result[1]["code"] == "line of code 2"


@pytest.mark.parametrize("search_term,commit_message,should_match", [
    ("test", "test commit", True),
    ("feat", "feat: new feature", True),
    ("bug", "random commit", False),
])
@patch("subprocess.run")
def test_should_find_commits_based_on_message(mock_run, git_commit_line, search_term, commit_message, should_match):
    """
    Test that find_commit correctly searches commits based on message content.
    Verifies that search matches are properly identified in commit messages.
    """
    if should_match:
        mock_run.return_value.stdout = git_commit_line.replace("message1", commit_message)
    else:
        mock_run.return_value.stdout = ""  # No matches found
    result = find_commit(search_term)
    assert bool(len(result)) == should_match
    if should_match:
        assert result[0]["message"] == commit_message
