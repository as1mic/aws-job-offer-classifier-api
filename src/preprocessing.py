import re


def clean_text(text: str) -> str:
    """Basic text cleanup that keeps useful technical markers."""
    if not text:
        return ""

    cleaned = text.lower()
    cleaned = re.sub(r"[^a-z0-9\s\+\#\.\-/]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()