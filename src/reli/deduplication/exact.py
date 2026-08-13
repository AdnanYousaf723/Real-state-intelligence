def generate_canonical_key(normalized_address: str, city: str, state: str, zip_code: str) -> str:
    """
    Generates a predictable, unique string for level-2 deduplication.
    Example: 123-main-st|denver|co|80202
    """
    if not normalized_address or not city or not state or not zip_code:
        return ""
    
    addr = normalized_address.replace(" ", "-").lower()
    c = city.lower().strip().replace(" ", "-")
    s = state.lower().strip()
    z = str(zip_code).strip()
    
    return f"{addr}|{c}|{s}|{z}"
