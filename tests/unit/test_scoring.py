from reli.scoring.scorer import LeadScorer
from reli.scoring.rules import get_ownership_points

def test_ownership_points():
    assert get_ownership_points(25.0) == 25
    assert get_ownership_points(16.0) == 15
    assert get_ownership_points(10.0) == 0

def test_score_property():
    scorer = LeadScorer()
    
    signals = [
        {"signal_type": "ABSENTEE_OWNER", "value_numeric": None, "evidence": "Absentee"},
        {"signal_type": "LONG_OWNERSHIP", "value_numeric": 21.0, "evidence": "21 years"}
    ]
    
    result = scorer.score_property(signals)
    
    assert result["score"] == 40  # 15 + 25
    assert result["priority"] == "MEDIUM"
    assert "Absentee" in result["reasons"]
    assert "21 years" in result["reasons"]

def test_score_capping():
    scorer = LeadScorer()
    
    signals = [
        {"signal_type": "ABSENTEE_OWNER", "value_numeric": None, "evidence": "Absentee"},
        {"signal_type": "LONG_OWNERSHIP", "value_numeric": 21.0, "evidence": "21 years"},
        {"signal_type": "VACANCY_SIGNAL", "value_numeric": None, "evidence": "Vacant"},
        {"signal_type": "TAX_SIGNAL", "value_numeric": None, "evidence": "Tax"},
        {"signal_type": "DISTRESS_SIGNAL", "value_numeric": None, "evidence": "Distress"}
    ]
    
    result = scorer.score_property(signals)
    
    # 15 + 25 + 25 + 20 + 15 = 100
    assert result["score"] == 100
    assert result["priority"] == "VERY_HIGH"
