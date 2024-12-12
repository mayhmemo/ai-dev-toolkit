from typing import Union
from pydantic import ValidationError


def is_valid_diff(diff_content: str) -> Union[bool, str]:
    if not diff_content:
        return "Diff content cannot be empty"

    if diff_content.isspace():
        return "Diff must start with 'diff', '---', or '+++'"

    lines = diff_content.splitlines()
    first_line = lines[0].strip()
    if not first_line:
        return "Diff must start with 'diff', '---', or '+++'"

    if not first_line.startswith(("diff", "---", "+++")):
        return "Diff must start with 'diff', '---', or '+++'"

    has_hunk = False
    for i, line in enumerate(lines, 1):
        if line.startswith("@@"):
            has_hunk = True
            parts = line.split("@@")
            if len(parts) < 3:
                return f"Invalid hunk header format at line {i}: {line}"
            try:
                old_start = parts[1].split()[0]
                new_start = parts[1].split()[1]
                if not (old_start.startswith("-") and new_start.startswith("+")):
                    return f"Invalid line numbers in hunk header at line {i}: {line}"
            except (IndexError, ValueError):
                return f"Invalid hunk header format at line {i}: {line}"
        elif line and not line.startswith((" ", "+", "-", "\\", "diff", "---", "+++")):
            return f"Invalid line prefix at line {i}: {line}"

    if not has_hunk:
        return "Diff must contain at least one hunk (@@ section)"

    return True
