import pytest
from pathlib import Path
from ai_dev_toolkit.utils.git.valid import is_valid_diff


def test_empty_diff():
    assert is_valid_diff("") == "Diff content cannot be empty"


def test_whitespace_diff():
    assert is_valid_diff("   \n  ") == "Diff must start with 'diff', '---', or '+++'"


def test_invalid_start():
    assert is_valid_diff("invalid start") == "Diff must start with 'diff', '---', or '+++'"


def test_empty_first_line():
    assert is_valid_diff("\nrest of diff") == "Diff must start with 'diff', '---', or '+++'"


def test_valid_diff_start():
    diff_file = Path(__file__).parent / "diffs" / "test_valid_diff_start.diff"
    with open(diff_file) as f:
        valid_diff = f.read()
    assert is_valid_diff(valid_diff) is True


def test_invalid_hunk_header():
    diff_file = Path(__file__).parent / "diffs" / "test_invalid_hunk_header.diff"
    with open(diff_file) as f:
        invalid_diff = f.read()
    result = is_valid_diff(invalid_diff)
    assert result.startswith("Invalid hunk header format")


def test_invalid_line_numbers():
    diff_file = Path(__file__).parent / "diffs" / "test_invalid_line_numbers.diff"
    with open(diff_file) as f:
        invalid_diff = f.read()
    assert "Invalid line numbers in hunk header" in is_valid_diff(invalid_diff)


def test_invalid_line_prefix():
    diff_file = Path(__file__).parent / "diffs" / "test_invalid_line_prefix.diff"
    with open(diff_file) as f:
        invalid_diff = f.read()
    assert "Invalid line prefix at line" in is_valid_diff(invalid_diff)


def test_no_hunks():
    diff_file = Path(__file__).parent / "diffs" / "test_no_hunks.diff"
    with open(diff_file) as f:
        invalid_diff = f.read()
    assert is_valid_diff(invalid_diff) == "Diff must contain at least one hunk (@@ section)"


def test_valid_complex_diff():
    diff_file = Path(__file__).parent / "diffs" / "test_valid_complex_diff.diff"
    with open(diff_file) as f:
        valid_diff = f.read()
    assert is_valid_diff(valid_diff) is True


def test_invalid_hunk_header_missing_parts():
    invalid_diff = """diff --git a/file1 b/file2
--- a/file1
+++ b/file2
@@ -1,3 @@"""
    result = is_valid_diff(invalid_diff)
    assert result.startswith("Invalid hunk header format")
