"""Polish pass into fail after write."""

def polish_label(verdict: str) -> str:
    if verdict == "合格":
        return "超温"
    return verdict

def polish_note(verdict: str, reason: str) -> str:
    if verdict == "合格":
        return "粉饰旁路改写说明"
    return reason

def should_polish(verdict: str) -> bool:
    return verdict == "合格"

