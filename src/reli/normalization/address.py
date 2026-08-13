import re

def normalize_address(address: str) -> str:
    """Normalizes address strings for consistent canonical key generation."""
    if not isinstance(address, str) or not address:
        return ""
    
    # 1. Lowercase
    addr = address.lower()
    
    # 2. Strip whitespace
    addr = addr.strip()
    
    # 3. Remove unnecessary punctuation
    addr = re.sub(r'[.,]', '', addr)
    
    # 4. Normalize common street suffixes
    suffix_map = {
        r'\bstreet\b': 'st',
        r'\bavenue\b': 'ave',
        r'\bboulevard\b': 'blvd',
        r'\bdrive\b': 'dr',
        r'\broad\b': 'rd',
        r'\blane\b': 'ln',
        r'\bcourt\b': 'ct',
        r'\bplace\b': 'pl',
        r'\bcircle\b': 'cir',
        r'\bhighway\b': 'hwy'
    }
    
    for pattern, replacement in suffix_map.items():
        addr = re.sub(pattern, replacement, addr)
        
    # 5. Normalize directional abbreviations
    directional_map = {
        r'\bnorth\b': 'n',
        r'\bsouth\b': 's',
        r'\beast\b': 'e',
        r'\bwest\b': 'w'
    }
    
    for pattern, replacement in directional_map.items():
        addr = re.sub(pattern, replacement, addr)
    
    # 6. Remove extra spaces (collapse multiple spaces to one)
    addr = re.sub(r'\s+', ' ', addr)
    
    return addr
