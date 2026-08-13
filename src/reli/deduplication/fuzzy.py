import difflib

def calculate_similarity(address1: str, address2: str) -> float:
    """
    Calculates the Levenshtein-like string similarity ratio between two addresses.
    Uses Python's built-in difflib for zero-dependency implementation in MVP.
    """
    if not address1 or not address2:
        return 0.0
    return difflib.SequenceMatcher(None, address1.lower(), address2.lower()).ratio()
