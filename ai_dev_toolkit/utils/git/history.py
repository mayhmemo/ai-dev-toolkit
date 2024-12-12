import subprocess
from typing import List, Dict
from datetime import datetime


def get_file_history(file: str) -> List[Dict]:
    """Gets commit history for a file"""
    try:
        result = subprocess.run(
            ["git", "log", "--follow", "--pretty=format:%H|%an|%ae|%at|%s", "--", file],
            capture_output=True,
            text=True,
            check=True,
        )

        commits = []
        for line in result.stdout.splitlines():
            if not line:
                continue

            hash_, author, email, timestamp, message = line.split("|")
            commits.append(
                {
                    "hash": hash_,
                    "author": author,
                    "email": email,
                    "date": datetime.fromtimestamp(int(timestamp)),
                    "message": message,
                }
            )

        return commits
    except subprocess.CalledProcessError:
        return []


def blame(file: str) -> List[Dict]:
    """Gets blame information for a file"""
    try:
        result = subprocess.run(
            ["git", "blame", "--porcelain", file],
            capture_output=True,
            text=True,
            check=True,
        )

        blame_info = []
        current_commit = None

        for line in result.stdout.splitlines():
            # Start of a new commit
            if line.startswith(tuple("0123456789abcdef")) and len(line.split()) >= 4:
                if current_commit and "code" in current_commit:
                    blame_info.append(current_commit)
                current_commit = {
                    "hash": line.split()[0],
                    "line_number": len(blame_info) + 1,
                }
            # Author information
            elif line.startswith("author ") and current_commit:
                current_commit["author"] = line[7:]  # Skip 'author '
            elif line.startswith("author-mail ") and current_commit:
                current_commit["email"] = line[12:]  # Skip 'author-mail '
            elif line.startswith("author-time ") and current_commit:
                timestamp = int(line[12:])  # Skip 'author-time '
                current_commit["date"] = datetime.fromtimestamp(timestamp)
            elif line.startswith("summary ") and current_commit:
                current_commit["message"] = line[8:]  # Skip 'summary '
            # Code line
            elif line.startswith("\t") and current_commit:
                current_commit["code"] = line[1:]  # Skip tab

        # Add the last commit if it exists and has code
        if current_commit and "code" in current_commit:
            blame_info.append(current_commit)

        return blame_info
    except subprocess.CalledProcessError:
        return []


def find_commit(message: str) -> List[str]:
    """Searches commits by message"""
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--all",
                "--grep",
                message,
                "--pretty=format:%H|%an|%ae|%at|%s",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        commits = []
        for line in result.stdout.splitlines():
            if not line:
                continue

            hash_, author, email, timestamp, msg = line.split("|")
            commit_info = {
                "hash": hash_,
                "author": author,
                "email": email,
                "date": datetime.fromtimestamp(int(timestamp)),
                "message": msg,
            }
            commits.append(commit_info)

        return commits
    except subprocess.CalledProcessError:
        return []
