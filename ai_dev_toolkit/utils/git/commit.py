from typing import Optional
import subprocess
from pathlib import Path


def generate_smart_commit_message(diff: str) -> str:
    """Analyzes the changes and generates a descriptive commit message"""
    # TODO: Implement AI-based analysis of the diff
    # For now, return a basic message
    if not diff:
        return "Empty commit"

    lines = diff.splitlines()
    files_changed = sum(1 for line in lines if line.startswith("+++"))
    return f"Update {files_changed} files"


def commit_changes(message: str, files: list[str]) -> bool:
    """Creates a commit with the given message and files"""
    try:
        if files:
            subprocess.run(["git", "add", *files], check=True)

        subprocess.run(["git", "commit", "-m", message], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def amend_commit(message: Optional[str] = None) -> bool:
    """Amends the last commit with new changes and/or message"""
    try:
        cmd = ["git", "commit", "--amend"]
        if message:
            cmd.extend(["-m", message])
        else:
            cmd.append("--no-edit")

        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
