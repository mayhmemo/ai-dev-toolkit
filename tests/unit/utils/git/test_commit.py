import subprocess
from unittest.mock import patch
from ai_dev_toolkit.utils.git.commit import generate_smart_commit_message, commit_changes, amend_commit


def test_generate_smart_commit_message_empty():
    assert generate_smart_commit_message("") == "Empty commit"


def test_generate_smart_commit_message_with_files():
    diff = """diff --git a/file1 b/file1
--- a/file1
+++ b/file1
@@ -1,3 +1,3 @@
 line1
-line2
+line2 modified
diff --git a/file2 b/file2
--- a/file2
+++ b/file2
"""
    assert generate_smart_commit_message(diff) == "Update 2 files"


@patch("subprocess.run")
def test_commit_changes_with_files(mock_run):
    mock_run.return_value.returncode = 0
    assert commit_changes("test message", ["file1.txt", "file2.txt"]) is True
    assert mock_run.call_count == 2


@patch("subprocess.run")
def test_commit_changes_without_files(mock_run):
    mock_run.return_value.returncode = 0
    assert commit_changes("test message", []) is True
    assert mock_run.call_count == 1


@patch("subprocess.run")
def test_commit_changes_failure(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
    assert commit_changes("test message", ["file1.txt"]) is False


@patch("subprocess.run")
def test_amend_commit_with_message(mock_run):
    mock_run.return_value.returncode = 0
    assert amend_commit("new message") is True
    mock_run.assert_called_once_with(
        ["git", "commit", "--amend", "-m", "new message"],
        check=True
    )


@patch("subprocess.run")
def test_amend_commit_without_message(mock_run):
    mock_run.return_value.returncode = 0
    assert amend_commit() is True
    mock_run.assert_called_once_with(
        ["git", "commit", "--amend", "--no-edit"],
        check=True
    )


@patch("subprocess.run")
def test_amend_commit_failure(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
    assert amend_commit("new message") is False
