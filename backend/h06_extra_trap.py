from pass_polish import polish_label, polish_note, should_polish

def after_write(verdict: str, reason: str):
    if should_polish(verdict):
        return polish_label(verdict), polish_note(verdict, reason)
    return verdict, reason

