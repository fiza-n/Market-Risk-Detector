from price_intelligence.reference_data import get_reference

def analyze_price(price: float, category: str) -> dict:
    """
    Returns the price_analysis object per Shared_Data_Contract.md §3:
    { price_deviation_score, price_flags, category_reference_range }
    """
    ref = get_reference(category)
    if not ref or (ref["typical_min_price"] == 0 and ref["typical_max_price"] == 0):
        return {
            "price_deviation_score": 0, 
            "price_flags": [], 
            "category_reference_range": {"min": 0, "max": 0}
        }

    avg = (ref["typical_min_price"] + ref["typical_max_price"]) / 2
    deviation_pct = ((avg - price) / avg) * 100

    flags = []
    score = 0

    if deviation_pct > 30:
        score = min(int(deviation_pct), 100)
        flags.append(f"price {round(deviation_pct)}% below category average")
    elif deviation_pct < -50:
        score = min(int(abs(deviation_pct) / 2), 100)
        flags.append(f"price {round(abs(deviation_pct))}% above category average")

    return {
        "price_deviation_score": score,
        "price_flags": flags,
        "category_reference_range": {
            "min": ref["typical_min_price"],
            "max": ref["typical_max_price"]
        }
    }