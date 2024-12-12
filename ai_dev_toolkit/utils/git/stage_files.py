import subprocess
from typing import List
from pathlib import Path


def stage_files(files: List[str]) -> bool:
    """Stages the specified files for commit"""
    try:
        if not files:
            return False
        subprocess.run(["git", "add", *files], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def unstage_files(files: List[str]) -> bool:
    """Unstages the specified files"""
    try:
        if not files:
            return False
        subprocess.run(["git", "reset", "HEAD", *files], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def stage_hunks(file: str, hunks: List[str]) -> bool:
    """Stages specific hunks from a file"""
    try:
        # Create a patch from the hunks
        patch_content = "\n".join(hunks)

        # Use git apply to apply the patch
        process = subprocess.Popen(
            ["git", "apply", "--cached", "--unidiff-zero"],
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        _, stderr = process.communicate(input=patch_content.encode())

        return process.returncode == 0
    except (subprocess.SubprocessError, OSError):
        return False
