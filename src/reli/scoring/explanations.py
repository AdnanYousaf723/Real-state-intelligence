from typing import List, Dict, Any

def generate_reason_summary(applied_rules: List[Dict[str, Any]]) -> str:
    """
    Takes a list of applied signals and their points to generate an explainable human-readable summary.
    """
    if not applied_rules:
        return "No prioritizing signals detected."
        
    reasons = ["High-priority because:"]
    for rule in applied_rules:
        # e.g., "• Property is marked as absentee-owned in the source record. (+15)"
        reasons.append(f"• {rule['evidence']} (+{rule['points']})")
        
    return "\n".join(reasons)
