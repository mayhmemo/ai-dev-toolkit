import subprocess
from typing import Dict, List
import re
from pathlib import Path


def analyze_changes(diff: str) -> Dict:
    """Analyzes changes for code review"""
    analysis = {
        "files_changed": 0,
        "insertions": 0,
        "deletions": 0,
        "file_types": {},
        "complexity": {"high_impact_files": [], "risky_patterns": []},
    }

    if not diff:
        return analysis

    lines = diff.splitlines()
    current_file = None

    for line in lines:
        if line.startswith("diff --git"):
            analysis["files_changed"] += 1
            current_file = line.split()[-1].lstrip("b/")
            ext = Path(current_file).suffix
            analysis["file_types"][ext] = analysis["file_types"].get(ext, 0) + 1
        elif line.startswith("+") and not line.startswith("+++"):
            analysis["insertions"] += 1
            # Check for risky patterns in added lines only
            risky_patterns = [
                r"TODO",
                r"FIXME",
                r"console\.log",
                r"print\(",
                r"debugger",
            ]

            for pattern in risky_patterns:
                if re.search(pattern, line[1:]):  # Skip the '+' character
                    pattern_msg = f"{current_file}: {pattern}"
                    if pattern_msg not in analysis["complexity"]["risky_patterns"]:
                        analysis["complexity"]["risky_patterns"].append(pattern_msg)

        elif line.startswith("-") and not line.startswith("---"):
            analysis["deletions"] += 1

    # Identify high impact files (many changes)
    if analysis["insertions"] + analysis["deletions"] > 100:
        analysis["complexity"]["high_impact_files"].append(current_file)

    return analysis


def suggest_reviewers(diff: str) -> List[str]:
    """Suggests reviewers based on changed files"""
    try:
        files = []
        for line in diff.splitlines():
            if line.startswith("diff --git"):
                files.append(line.split()[-1].lstrip("b/"))

        reviewers = set()
        for file in files:
            blame = subprocess.run(
                ["git", "blame", "--porcelain", file], capture_output=True, text=True
            )
            if blame.returncode == 0:
                for line in blame.stdout.splitlines():
                    if line.startswith("author "):
                        reviewers.add(line.split("author ")[1])

        # Sort by frequency of contributions
        return sorted(list(reviewers))
    except subprocess.CalledProcessError:
        return []


def impact_analysis(diff: str) -> Dict:
    """Analyzes impact of changes"""
    impact = {
        "scope": {"files": [], "directories": set()},
        "dependencies": {"added": [], "removed": []},
        "api_changes": [],
        "test_coverage": {"modified_tests": [], "needs_tests": []},
    }

    lines = diff.splitlines()
    current_file = None

    for line in lines:
        if line.startswith("diff --git"):
            current_file = line.split()[-1].lstrip("b/")
            impact["scope"]["files"].append(current_file)
            impact["scope"]["directories"].add(str(Path(current_file).parent))
            # Add test files to modified_tests only when we first encounter them
            if "test" in current_file.lower():
                impact["test_coverage"]["modified_tests"].append(current_file)

        # Check for dependency changes
        if "requirements.txt" in current_file or "package.json" in current_file:
            if line.startswith("+") and not line.startswith("+++"):
                # Only add actual package lines, not file paths
                if "==" in line or "@" in line:
                    impact["dependencies"]["added"].append(line[1:].strip())
            elif line.startswith("-") and not line.startswith("---"):
                if "==" in line or "@" in line:
                    impact["dependencies"]["removed"].append(line[1:].strip())

        # Check for API changes
        api_patterns = [
            r"@api",
            r"def \w+\(",
            r"class \w+",
            r"interface \w+",
            r"function \w+\(",
        ]

        for pattern in api_patterns:
            if re.search(pattern, line):
                impact["api_changes"].append(f"{current_file}: {line.strip()}")

        # Check for files that need tests
        if line.startswith("+") and not any(
            test in current_file for test in ["test", "spec", "_test"]
        ):
            if current_file not in impact["test_coverage"]["needs_tests"]:
                impact["test_coverage"]["needs_tests"].append(current_file)

    impact["scope"]["directories"] = list(impact["scope"]["directories"])
    return impact
