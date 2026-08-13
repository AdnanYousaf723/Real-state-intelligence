# Scoring version v1.0 based on specification rules
SCORING_VERSION = "1.0"

# Define base points for binary signals
SIGNAL_POINTS = {
    "ABSENTEE_OWNER": 15,
    "VACANCY_SIGNAL": 25,
    "TAX_SIGNAL": 20,
    "DISTRESS_SIGNAL": 15,
}

def get_ownership_points(years: float) -> int:
    if years >= 20.0:
        return 25
    elif years >= 15.0:
        return 15
    return 0
