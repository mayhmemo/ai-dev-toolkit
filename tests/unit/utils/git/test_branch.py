import subprocess
from unittest.mock import patch
from ai_dev_toolkit.utils.git.branch import (
    create_branch,
    switch_branch,
    merge_branch,
    list_branches,
    delete_branch,
)


@patch("subprocess.run")
def test_create_branch_creates_new_branch_from_current_head(mock_run):
    mock_run.return_value.returncode = 0
    assert create_branch("feature-branch") is True
    mock_run.assert_called_once_with(
        ["git", "checkout", "-b", "feature-branch"], check=True
    )


@patch("subprocess.run")
def test_create_branch_creates_new_branch_from_specified_base(mock_run):
    mock_run.return_value.returncode = 0
    assert create_branch("feature-branch", "main") is True
    mock_run.assert_called_once_with(
        ["git", "checkout", "-b", "feature-branch", "main"], check=True
    )


@patch("subprocess.run")
def test_create_branch_returns_false_when_git_command_fails(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "git")
    assert create_branch("feature-branch") is False


@patch("subprocess.run")
def test_switch_branch_changes_to_specified_branch(mock_run):
    mock_run.return_value.returncode = 0
    assert switch_branch("main") is True
    mock_run.assert_called_once_with(["git", "checkout", "main"], check=True)


@patch("subprocess.run")
def test_switch_branch_returns_false_when_branch_not_exists(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "git")
    assert switch_branch("non-existent") is False


@patch("subprocess.run")
def test_merge_branch_merges_source_into_current_branch(mock_run):
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "Fast-forward merge successful"
    success, message = merge_branch("feature-branch")
    assert success is True
    assert message == "Fast-forward merge successful"
    mock_run.assert_called_with(
        ["git", "merge", "feature-branch"], capture_output=True, text=True, check=True
    )


@patch("subprocess.run")
def test_merge_branch_switches_to_target_before_merging(mock_run):
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "Merge successful"
    success, message = merge_branch("feature-branch", "main")
    assert success is True
    assert message == "Merge successful"
    assert mock_run.call_count == 2
    mock_run.assert_any_call(["git", "checkout", "main"], check=True)
    mock_run.assert_any_call(
        ["git", "merge", "feature-branch"], capture_output=True, text=True, check=True
    )


@patch("subprocess.run")
def test_merge_branch_returns_false_and_error_message_on_conflict(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(
        1, "git", stderr="Merge conflict"
    )
    success, message = merge_branch("feature-branch")
    assert success is False
    assert message == "Merge conflict"


@patch("subprocess.run")
def test_list_branches_returns_all_local_branches(mock_run):
    mock_run.return_value.stdout = "* main\n  feature-1\n  feature-2\n"
    branches = list_branches()
    assert branches == ["main", "feature-1", "feature-2"]
    mock_run.assert_called_once_with(
        ["git", "branch"], capture_output=True, text=True, check=True
    )


@patch("subprocess.run")
def test_list_branches_returns_all_remote_branches(mock_run):
    mock_run.return_value.stdout = "  origin/main\n  origin/feature-1\n"
    branches = list_branches(remote=True)
    assert branches == ["origin/main", "origin/feature-1"]
    mock_run.assert_called_once_with(
        ["git", "branch", "-r"], capture_output=True, text=True, check=True
    )


@patch("subprocess.run")
def test_list_branches_returns_empty_list_when_git_command_fails(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "git")
    assert list_branches() == []


@patch("subprocess.run")
def test_delete_branch_removes_specified_branch(mock_run):
    mock_run.return_value.returncode = 0
    assert delete_branch("feature-branch") is True
    mock_run.assert_called_once_with(
        ["git", "branch", "-d", "feature-branch"], check=True
    )


@patch("subprocess.run")
def test_delete_branch_force_removes_unmerged_branch(mock_run):
    mock_run.return_value.returncode = 0
    assert delete_branch("feature-branch", force=True) is True
    mock_run.assert_called_once_with(
        ["git", "branch", "-D", "feature-branch"], check=True
    )


@patch("subprocess.run")
def test_delete_branch_returns_false_when_git_command_fails(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "git")
    assert delete_branch("feature-branch") is False
