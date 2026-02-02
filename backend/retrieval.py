def similarity(a: str, b: str) -> float:
    """
    Very simple similarity:
    ratio of common words
    """
    if not a or not b:
        return 0.0

    set_a = set(a.lower().split())
    set_b = set(b.lower().split())

    return len(set_a & set_b) / max(len(set_a), 1)
