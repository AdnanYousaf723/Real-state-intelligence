from typing import List, Dict, Any
from .rules import SCORING_VERSION, SIGNAL_POINTS, get_ownership_points
from .explanations import generate_reason_summary

class LeadScorer:
    @staticmethod
    def calculate_priority(score: int) -> str:
        if score >= 85: return "VERY_HIGH"
        if score >= 70: return "HIGH"
        if score >= 40: return "MEDIUM"
        return "LOW"

    def score_property(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Consumes observable signals and generates a capped score, priority, and explanation.
        Avoids double-counting ownership rules by evaluating thresholds.
        """
        raw_score = 0
        applied_rules = []
        
        for sig in signals:
            sig_type = sig["signal_type"]
            points = 0
            
            if sig_type == "LONG_OWNERSHIP":
                years = sig.get("value_numeric", 0)
                points = get_ownership_points(years)
            elif sig_type in SIGNAL_POINTS:
                points = SIGNAL_POINTS[sig_type]
                
            if points > 0:
                raw_score += points
                applied_rules.append({
                    "signal_type": sig_type,
                    "points": points,
                    "evidence": sig["evidence"]
                })
        
        # Enforce max score cap of 100
        final_score = min(raw_score, 100)
        priority = self.calculate_priority(final_score)
        reasons = generate_reason_summary(applied_rules)
        
        return {
            "score": final_score,
            "priority": priority,
            "reasons": reasons,
            "scoring_version": SCORING_VERSION,
            "applied_signals": applied_rules
        }
