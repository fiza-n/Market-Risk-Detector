from price_intelligence.deviation import analyze_price


def test_underpriced_flags_correctly():
    result = analyze_price(45000, "Mobile Phones")
    print(result)
    assert result["price_deviation_score"] > 0
    assert len(result["price_flags"]) > 0


def test_normal_price_no_flags():
    result = analyze_price(120000, "Mobile Phones")
    print(result)
    assert result["price_deviation_score"] == 0
    assert result["price_flags"] == []


def test_unknown_category_returns_zero():
    result = analyze_price(50000, "Nonexistent Category")
    print(result)
    assert result["price_deviation_score"] == 0
    assert result["category_reference_range"] == {"min": 0, "max": 0}


if __name__ == "__main__":
    test_underpriced_flags_correctly()
    test_normal_price_no_flags()
    test_unknown_category_returns_zero()
    print("All tests passed!! ")