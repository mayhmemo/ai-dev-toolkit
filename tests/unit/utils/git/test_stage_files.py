from unittest.mock import patch, Mock, MagicMock
from ai_dev_toolkit.utils.git.stage_files import stage_files, unstage_files, stage_hunks
import subprocess
import pytest


def test_stage_files_returns_false_for_empty_file_list():
    assert stage_files([]) is False


@patch("subprocess.run")
def test_stage_files_adds_multiple_files_to_staging_area(mock_run):
    mock_run.return_value.returncode = 0
    assert stage_files(["file1.txt", "file2.txt"]) is True
    mock_run.assert_called_once_with(
        ["git", "add", "file1.txt", "file2.txt"], check=True
    )


@patch("subprocess.run")
def test_stage_files_returns_false_when_git_add_fails(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "git")
    assert stage_files(["file1.txt"]) is False


def test_unstage_files_returns_false_for_empty_file_list():
    assert unstage_files([]) is False


@patch("subprocess.run")
def test_unstage_files_removes_multiple_files_from_staging_area(mock_run):
    mock_run.return_value.returncode = 0
    assert unstage_files(["file1.txt", "file2.txt"]) is True
    mock_run.assert_called_once_with(
        ["git", "reset", "HEAD", "file1.txt", "file2.txt"], check=True
    )


@patch("subprocess.run")
def test_unstage_files_returns_false_when_git_reset_fails(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "git")
    assert unstage_files(["file1.txt"]) is False


@patch("subprocess.Popen")
def test_stage_hunks_applies_patch_to_staging_area(mock_popen):
    mock_process = Mock()
    mock_process.returncode = 0
    mock_process.communicate.return_value = (b"", b"")
    mock_popen.return_value = mock_process

    hunks = ["@@ -1,3 +1,3 @@", " unchanged", "-removed", "+added"]
    assert stage_hunks("file.txt", hunks) is True
    mock_popen.assert_called_once_with(
        ["git", "apply", "--cached", "--unidiff-zero"],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


@patch("subprocess.Popen")
def test_stage_hunks_returns_false_when_patch_application_fails(mock_popen):
    mock_process = Mock()
    mock_process.returncode = 1
    mock_process.communicate.return_value = (b"", b"error")
    mock_popen.return_value = mock_process

    assert stage_hunks("file.txt", ["invalid hunk"]) is False


@patch('subprocess.run')
def test_stage_files_empty_list(mock_run):
    assert stage_files([]) is False
    mock_run.assert_not_called()


@patch('subprocess.run')
def test_stage_files_success(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    assert stage_files(['file1.txt', 'file2.txt']) is True
    mock_run.assert_called_once_with(['git', 'add', 'file1.txt', 'file2.txt'], check=True)


@patch('subprocess.run')
def test_stage_files_failure(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
    assert stage_files(['file1.txt']) is False


@patch('subprocess.run')
def test_unstage_files_empty_list(mock_run):
    assert unstage_files([]) is False
    mock_run.assert_not_called()


@patch('subprocess.run')
def test_unstage_files_success(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    assert unstage_files(['file1.txt', 'file2.txt']) is True
    mock_run.assert_called_once_with(['git', 'reset', 'HEAD', 'file1.txt', 'file2.txt'], check=True)


@patch('subprocess.run')
def test_unstage_files_failure(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
    assert unstage_files(['file1.txt']) is False


@patch('subprocess.Popen')
def test_stage_hunks_success(mock_popen):
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.communicate.return_value = (b'', b'')
    mock_popen.return_value = mock_process

    hunks = [
        '@@ -1,3 +1,3 @@\n unchanged\n-removed\n+added\n'
    ]
    assert stage_hunks('file.txt', hunks) is True
    mock_popen.assert_called_once_with(
        ['git', 'apply', '--cached', '--unidiff-zero'],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


@patch('subprocess.Popen')
def test_stage_hunks_failure(mock_popen):
    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_process.communicate.return_value = (b'', b'error')
    mock_popen.return_value = mock_process

    hunks = ['invalid hunk']
    assert stage_hunks('file.txt', hunks) is False


@patch('subprocess.Popen')
def test_stage_hunks_subprocess_error(mock_popen):
    mock_popen.side_effect = subprocess.SubprocessError()
    assert stage_hunks('file.txt', ['hunk']) is False


@patch('subprocess.Popen')
def test_stage_hunks_os_error(mock_popen):
    mock_popen.side_effect = OSError()
    assert stage_hunks('file.txt', ['hunk']) is False
