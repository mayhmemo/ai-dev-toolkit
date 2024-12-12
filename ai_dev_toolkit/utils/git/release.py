import subprocess
from typing import List, Tuple
import re
from pathlib import Path


def bump_version(version_type: str) -> str:
    """Bumps version according to semver"""
    try:
        # Try to find version in common files
        version_files = ["setup.py", "package.json", "VERSION", "__init__.py"]

        version_pattern = r"(\d+)\.(\d+)\.(\d+)"
        current_version = None
        version_file = None

        for file in version_files:
            if Path(file).exists():
                with open(file, "r") as f:
                    content = f.read()
                    match = re.search(version_pattern, content)
                    if match:
                        current_version = match.group(0)
                        version_file = file
                        break

        if not current_version:
            return ""

        # Parse version
        major, minor, patch = map(int, current_version.split("."))

        # Bump according to type
        if version_type == "major":
            major += 1
            minor = patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1

        new_version = f"{major}.{minor}.{patch}"

        # Update version in file
        with open(version_file, "r") as f:
            content = f.read()

        new_content = re.sub(version_pattern, new_version, content)

        with open(version_file, "w") as f:
            f.write(new_content)

        return new_version
    except (IOError, subprocess.CalledProcessError):
        return ""


def generate_changelog(from_ref: str, to_ref: str) -> str:
    """Generates changelog between refs"""
    try:
        result = subprocess.run(
            ["git", "log", f"{from_ref}..{to_ref}", "--pretty=format:%s"],
            capture_output=True,
            text=True,
            check=True,
        )

        commits = result.stdout.splitlines()
        changelog = []

        # Categorize commits
        features = []
        fixes = []
        others = []

        for commit in commits:
            if commit.lower().startswith(("feat", "feature")):
                features.append(commit)
            elif commit.lower().startswith(("fix", "bug")):
                fixes.append(commit)
            else:
                others.append(commit)

        # Format changelog
        if features:
            changelog.extend(["### Features", *[f"- {c}" for c in features], ""])
        if fixes:
            changelog.extend(["### Bug Fixes", *[f"- {c}" for c in fixes], ""])
        if others:
            changelog.extend(["### Other Changes", *[f"- {c}" for c in others], ""])

        return "\n".join(changelog)
    except subprocess.CalledProcessError:
        return ""


def detect_breaking_changes(diff: str) -> List[str]:
    """Detects potential breaking changes"""
    breaking_changes = []

    if not diff:
        return breaking_changes

    lines = diff.splitlines()
    current_file = None

    breaking_patterns = [
        (r"class \w+", "Class definition changed"),
        (r"def \w+\([^)]*\)", "Function signature changed"),
        (r"interface \w+", "Interface changed"),
        (r"@api", "API definition changed"),
        (r"BREAKING CHANGE", "Breaking change noted in commit"),
        (r"deprecate", "Deprecation notice added"),
    ]

    for line in lines:
        if line.startswith("diff --git"):
            current_file = line.split()[-1].lstrip("b/")
        elif line.startswith("-") or line.startswith("+"):
            for pattern, message in breaking_patterns:
                if re.search(pattern, line):
                    change_msg = f"{current_file}: {message}"
                    if change_msg not in breaking_changes:
                        breaking_changes.append(change_msg)

    return breaking_changes


def update_dependencies() -> Tuple[bool, List[str]]:
    """Updates project dependencies"""
    updated = []
    success = True

    try:
        # Check for package.json
        if Path("package.json").exists():
            result = subprocess.run(["npm", "outdated"], capture_output=True, text=True)
            if result.returncode == 0:
                try:
                    subprocess.run(["npm", "update"], check=True)
                    updated.append("Updated npm packages")
                except subprocess.CalledProcessError:
                    updated.append("Failed to update npm packages")
                    success = False

        # Check for requirements.txt
        if Path("requirements.txt").exists():
            result = subprocess.run(
                ["pip", "list", "--outdated"], capture_output=True, text=True
            )
            if result.returncode == 0:
                try:
                    subprocess.run(
                        ["pip", "install", "-r", "requirements.txt", "--upgrade"],
                        check=True,
                    )
                    updated.append("Updated pip packages")
                except subprocess.CalledProcessError:
                    updated.append("Failed to update pip packages")
                    success = False

        return success, updated
    except subprocess.CalledProcessError:
        return False, updated
