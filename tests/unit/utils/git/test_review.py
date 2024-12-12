from unittest.mock import patch
from ai_dev_toolkit.utils.git.review import analyze_changes, suggest_reviewers, impact_analysis
import subprocess
from pathlib import Path


def test_analyze_changes_returns_empty_analysis_for_empty_diff():
    result = analyze_changes("")
    assert result == {
        "files_changed": 0,
        "insertions": 0,
        "deletions": 0,
        "file_types": {},
        "complexity": {"high_impact_files": [], "risky_patterns": []},
    }


def test_analyze_changes_detects_risky_patterns_and_file_types():
    diff_file = Path(__file__).parent / "diffs" / "test_analyze_changes_detects_risky_patterns_and_file_types.diff"
    with open(diff_file) as f:
        diff = f.read()

    result = analyze_changes(diff)
    assert result["files_changed"] == 2
    assert result["insertions"] == 4
    assert result["deletions"] == 1
    assert result["file_types"] == {".py": 1, ".js": 1}
    assert len(result["complexity"]["risky_patterns"]) == 4


def test_analyze_changes_identifies_high_impact_files():
    diff = "diff --git a/large_file.py b/large_file.py\n" + "+ new line\n" * 101
    result = analyze_changes(diff)
    assert "large_file.py" in result["complexity"]["high_impact_files"]


def test_suggest_reviewers_returns_sorted_list_of_unique_authors():
    diff = "diff --git a/test.py b/test.py"
    blame_output = """author Alice
author Bob
author Alice
author Charlie"""

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = blame_output
        result = suggest_reviewers(diff)
        assert result == ["Alice", "Bob", "Charlie"]


def test_suggest_reviewers_returns_empty_list_when_git_command_fails():
    diff = "diff --git a/test.py b/test.py"
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "git blame")
        result = suggest_reviewers(diff)
        assert result == []


def test_impact_analysis_detects_scope_dependencies_and_api_changes():
    diff_file = Path(__file__).parent / "diffs" / "test_impact_analysis_detects_scope_dependencies_and_api_changes.diff"
    with open(diff_file) as f:
        diff = f.read()

    result = impact_analysis(diff)
    assert len(result["scope"]["files"]) == 3
    assert len(result["dependencies"]["added"]) == 1
    assert len(result["dependencies"]["removed"]) == 1
    assert len(result["api_changes"]) == 2
    assert len(result["test_coverage"]["modified_tests"]) == 1


def test_impact_analysis_returns_empty_analysis_for_empty_diff():
    result = impact_analysis("")
    assert result == {
        "scope": {"files": [], "directories": []},
        "dependencies": {"added": [], "removed": []},
        "api_changes": [],
        "test_coverage": {"modified_tests": [], "needs_tests": []},
    }
