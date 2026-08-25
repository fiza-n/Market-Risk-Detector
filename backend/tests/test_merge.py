from merge.combine import combine_results


def test_weighted_score_calculation():
    price_analysis = {"price_deviation_score": 20, "price_flags": []}
    scam_analysis = {"scam_score": 50, "scam_flags": [], "tip": "Be careful"}
    result = combine_results(price_analysis, scam_analysis)
    # risk_penalty = round(20*0.4 + 50*0.6) = round(8 + 30) = 38
    # final_score = 100 - 38 = 62
    assert result["score"] == 62
    assert result["verdict"] == "medium_risk"


def test_verdict_boundary_low_risk_at_70():
    # risk_penalty = round(0*0.4 + 50*0.6) = 30 -> score = 70 exactly
    price_analysis = {"price_deviation_score": 0, "price_flags": []}
    scam_analysis = {"scam_score": 50, "scam_flags": [], "tip": "ok"}
    result = combine_results(price_analysis, scam_analysis)
    assert result["score"] == 70
    assert result["verdict"] == "low_risk"


def test_verdict_boundary_medium_risk_at_69():
    # risk_penalty = round(10*0.4 + 45*0.6) = round(4 + 27) = 31 -> score = 69
    price_analysis = {"price_deviation_score": 10, "price_flags": []}
    scam_analysis = {"scam_score": 45, "scam_flags": [], "tip": "ok"}
    result = combine_results(price_analysis, scam_analysis)
    assert result["score"] == 69
    assert result["verdict"] == "medium_risk"


def test_verdict_boundary_medium_risk_at_40():
    # risk_penalty = round(0*0.4 + 100*0.6) = 60 -> score = 40 exactly
    price_analysis = {"price_deviation_score": 0, "price_flags": []}
    scam_analysis = {"scam_score": 100, "scam_flags": [], "tip": "ok"}
    result = combine_results(price_analysis, scam_analysis)
    assert result["score"] == 40
    assert result["verdict"] == "medium_risk"


def test_verdict_boundary_high_risk_at_39():
    # risk_penalty = round(10*0.4 + 95*0.6) = round(4 + 57) = 61 -> score = 39
    price_analysis = {"price_deviation_score": 10, "price_flags": []}
    scam_analysis = {"scam_score": 95, "scam_flags": [], "tip": "ok"}
    result = combine_results(price_analysis, scam_analysis)
    assert result["score"] == 39
    assert result["verdict"] == "high_risk"


def test_flags_are_deduplicated_and_ordered():
    price_analysis = {"price_deviation_score": 30, "price_flags": ["Priced too low", "Shared flag"]}
    scam_analysis = {"scam_score": 30, "scam_flags": ["Shared flag", "Advance payment requested"], "tip": "ok"}
    result = combine_results(price_analysis, scam_analysis)
    assert result["flags"] == ["Priced too low", "Shared flag", "Advance payment requested"]


def test_no_flags_falls_back_to_default_message():
    price_analysis = {"price_deviation_score": 0, "price_flags": []}
    scam_analysis = {"scam_score": 0, "scam_flags": [], "tip": "ok"}
    result = combine_results(price_analysis, scam_analysis)
    assert result["flags"] == ["No explicit risk signals detected in listing."]


def test_tip_uses_scam_analysis_tip_when_present():
    price_analysis = {"price_deviation_score": 0, "price_flags": []}
    scam_analysis = {"scam_score": 0, "scam_flags": [], "tip": "Custom scam tip"}
    result = combine_results(price_analysis, scam_analysis)
    assert result["tip"] == "Custom scam tip"


def test_tip_falls_back_to_default_when_missing():
    price_analysis = {"price_deviation_score": 0, "price_flags": []}
    scam_analysis = {"scam_score": 0, "scam_flags": []}  # no "tip" key
    result = combine_results(price_analysis, scam_analysis)
    assert "Inspect item in person" in result["tip"]


def test_none_inputs_produce_safe_defaults():
    result = combine_results(None, None)
    assert result["score"] == 100
    assert result["verdict"] == "low_risk"
    assert result["flags"] == ["No explicit risk signals detected in listing."]
    assert "Inspect item in person" in result["tip"]


if __name__ == "__main__":
    test_weighted_score_calculation()
    test_verdict_boundary_low_risk_at_70()
    test_verdict_boundary_medium_risk_at_69()
    test_verdict_boundary_medium_risk_at_40()
    test_verdict_boundary_high_risk_at_39()
    test_flags_are_deduplicated_and_ordered()
    test_no_flags_falls_back_to_default_message()
    test_tip_uses_scam_analysis_tip_when_present()
    test_tip_falls_back_to_default_when_missing()
    test_none_inputs_produce_safe_defaults()
    print("All tests passed!!")