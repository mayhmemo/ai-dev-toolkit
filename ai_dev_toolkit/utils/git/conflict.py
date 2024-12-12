import subprocess
from typing import List
import re


def get_conflicts() -> List[str]:
    """Returns list of files with conflicts"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=U"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [file for file in result.stdout.splitlines() if file]
    except subprocess.CalledProcessError:
        return []


def resolve_conflict(file: str, resolution: str) -> bool:
    """Resolves a conflict in a file"""
    try:
        with open(file, "r") as f:
            content = f.read()

        # Find conflict markers
        conflict_pattern = r"<<<<<<< .*?\n(.*?)\n=======\n(.*?)>>>>>>> .*?\n"
        conflicts = list(re.finditer(conflict_pattern, content, re.DOTALL))

        if not conflicts:
            return False

        # Apply resolution
        new_content = content
        for match in reversed(conflicts):
            ours = match.group(1).rstrip()
            theirs = match.group(2).rstrip()

            if resolution == "ours":
                replacement = ours + "\n"
            elif resolution == "theirs":
                replacement = theirs + "\n"
            else:
                return False

            new_content = (
                new_content[: match.start()] + replacement + new_content[match.end() :]
            )

        # Write resolved content
        with open(file, "w") as f:
            f.write(new_content)

        # Stage the resolved file
        subprocess.run(["git", "add", file], check=True)
        return True
    except (subprocess.CalledProcessError, IOError):
        return False


def abort_merge() -> bool:
    """Aborts current merge operation"""
    try:
        subprocess.run(["git", "merge", "--abort"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
