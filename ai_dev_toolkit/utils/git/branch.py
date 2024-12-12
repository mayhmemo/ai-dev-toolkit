import subprocess
from typing import List, Tuple, Optional


def create_branch(name: str, base: Optional[str] = None) -> bool:
    """Creates a new branch"""
    try:
        cmd = ["git", "checkout", "-b", name]
        if base:
            cmd.append(base)
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def switch_branch(name: str) -> bool:
    """Switches to specified branch"""
    try:
        subprocess.run(["git", "checkout", name], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def merge_branch(source: str, target: Optional[str] = None) -> Tuple[bool, str]:
    """Merges source branch into target"""
    try:
        if target:
            subprocess.run(["git", "checkout", target], check=True)

        result = subprocess.run(
            ["git", "merge", source], capture_output=True, text=True, check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def list_branches(remote: bool = False) -> List[str]:
    """Lists all branches"""
    try:
        cmd = ["git", "branch"]
        if remote:
            cmd.append("-r")

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        branches = [branch.strip("* ") for branch in result.stdout.splitlines()]
        return branches
    except subprocess.CalledProcessError:
        return []


def delete_branch(name: str, force: bool = False) -> bool:
    """Deletes a branch"""
    try:
        cmd = ["git", "branch"]
        if force:
            cmd.append("-D")
        else:
            cmd.append("-d")
        cmd.append(name)

        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
