import subprocess
from unittest.mock import patch, mock_open
from ai_dev_toolkit.utils.git.release import (
    bump_version,
    generate_changelog,
    detect_breaking_changes,
    update_dependencies,
)
from pathlib import Path


@patch("pathlib.Path.exists")
@patch("builtins.open", new_callable=mock_open)
def test_bump_version_major(mock_file, mock_exists):
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = 'version = "1.2.3"'
    assert bump_version("major") == "2.0.0"


@patch("pathlib.Path.exists")
@patch("builtins.open", new_callable=mock_open)
def test_bump_version_minor(mock_file, mock_exists):
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = 'version = "1.2.3"'
    assert bump_version("minor") == "1.3.0"


@patch("pathlib.Path.exists")
@patch("builtins.open", new_callable=mock_open)
def test_bump_version_patch(mock_file, mock_exists):
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = 'version = "1.2.3"'
    assert bump_version("patch") == "1.2.4"


@patch("pathlib.Path.exists")
def test_bump_version_no_version_file(mock_exists):
    mock_exists.return_value = False
    assert bump_version("patch") == ""


@patch("pathlib.Path.exists")
@patch("builtins.open", new_callable=mock_open)
def test_bump_version_no_version_found(mock_file, mock_exists):
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = 'no version here'
    assert bump_version("patch") == ""


@patch("pathlib.Path.exists")
@patch("builtins.open")
def test_bump_version_io_error(mock_file, mock_exists):
    mock_exists.return_value = True
    mock_file.side_effect = IOError()
    assert bump_version("patch") == ""


@patch("subprocess.run")
def test_generate_changelog_with_all_types(mock_run):
    commits = """feat: new feature 1
fix: bug fix 1
other: some change
feat: new feature 2
fix: bug fix 2"""
    mock_run.return_value.stdout = commits
    changelog = generate_changelog("v1.0", "v2.0")
    assert "### Features" in changelog
    assert "- feat: new feature 1" in changelog
    assert "- feat: new feature 2" in changelog
    assert "### Bug Fixes" in changelog
    assert "- fix: bug fix 1" in changelog
    assert "- fix: bug fix 2" in changelog
    assert "### Other Changes" in changelog
    assert "- other: some change" in changelog


@patch("subprocess.run")
def test_generate_changelog_empty(mock_run):
    mock_run.return_value.stdout = ""
    assert generate_changelog("v1.0", "v2.0") == ""


@patch("subprocess.run")
def test_generate_changelog_error(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
    assert generate_changelog("v1.0", "v2.0") == ""


def test_detect_breaking_changes_empty():
    assert detect_breaking_changes("") == []


def test_detect_breaking_changes_class_change():
    diff = """diff --git a/file.py b/file.py
+++ b/file.py
--- a/file.py
@@ -1,1 +1,1 @@
-class OldName:
+class NewName:"""
    changes = detect_breaking_changes(diff)
    assert len(changes) == 1
    assert "file.py: Class definition changed" in changes


def test_detect_breaking_changes_function_signature():
    diff = """diff --git a/file.py b/file.py
+++ b/file.py
--- a/file.py
@@ -1,1 +1,1 @@
-def func():
+def func(new_param):"""
    changes = detect_breaking_changes(diff)
    assert len(changes) == 1
    assert "file.py: Function signature changed" in changes


def test_detect_breaking_changes_multiple_patterns():
    diff = """diff --git a/file.py b/file.py
+++ b/file.py
@@ -1,2 +1,2 @@
-class OldName:
-def func():
+class NewName:
+def func(new_param):"""
    changes = detect_breaking_changes(diff)
    assert len(changes) == 2


@patch("pathlib.Path.exists")
@patch("subprocess.run")
def test_update_dependencies_npm_success(mock_run, mock_exists):
    mock_exists.side_effect = [True, False]  # package.json exists, requirements.txt doesn't
    mock_run.return_value.returncode = 0
    success, updated = update_dependencies()
    assert success is True
    assert "Updated npm packages" in updated


@patch("pathlib.Path.exists")
@patch("subprocess.run")
def test_update_dependencies_pip_success(mock_run, mock_exists):
    mock_exists.side_effect = [False, True]  # package.json doesn't exist, requirements.txt does
    mock_run.return_value.returncode = 0
    success, updated = update_dependencies()
    assert success is True
    assert "Updated pip packages" in updated


@patch("pathlib.Path.exists")
@patch("subprocess.run")
def test_update_dependencies_both_fail(mock_run, mock_exists):
    mock_exists.side_effect = [True, True]  # Both package files exist
    mock_run.side_effect = [
        subprocess.CompletedProcess(args=[], returncode=0),  # npm outdated
        subprocess.CalledProcessError(1, "cmd"),  # npm update
        subprocess.CompletedProcess(args=[], returncode=0),  # pip list
        subprocess.CalledProcessError(1, "cmd"),  # pip install
    ]
    success, updated = update_dependencies()
    assert success is False
    assert "Failed to update npm packages" in updated
    assert "Failed to update pip packages" in updated


@patch("pathlib.Path.exists")
@patch("subprocess.run")
def test_update_dependencies_no_package_files(mock_run, mock_exists):
    mock_exists.return_value = False
    success, updated = update_dependencies()
    assert success is True
    assert not updated
