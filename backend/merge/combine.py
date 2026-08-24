"""
Merge logic: combines Person B's price deviation analysis and Person C's scam analysis
into the final score, verdict, flags, and tip JSON contract (Object #4).
"""

def combine_results(price_analysis=None, scam_analysis=None):
    """
    Combines price intelligence and scam detection outputs.
    
    :param price_analysis: Object #2 { price_deviation_score, price_flags, ... }
    :param scam_analysis: Object #3 { scam_score, scam_flags, tip, ... }
    :return: Object #4 { score, verdict, flags, tip }
    """
    price_score = price_analysis.get('price_deviation_score', 0) if price_analysis else 0
    scam_score = scam_analysis.get('scam_score', 0) if scam_analysis else 0

    price_flags = price_analysis.get('price_flags', []) if price_analysis else []
    scam_flags = scam_analysis.get('scam_flags', []) if scam_analysis else []

    # Final Trust Score calculation (100 = highest trust, 0 = highest risk)
    risk_penalty = round(price_score * 0.4 + scam_score * 0.6)
    final_score = max(0, min(100, 100 - risk_penalty))

    # Deduplicate flags while keeping original order
    combined_flags = []
    seen = set()
    for flag in price_flags + scam_flags:
        if flag and flag not in seen:
            seen.add(flag)
            combined_flags.append(flag)

    if not combined_flags:
        combined_flags.append("No explicit risk signals detected in listing.")

    # Determine verdict based on canonical spec thresholds
    if final_score >= 70:
        verdict = "low_risk"
    elif final_score >= 40:
        verdict = "medium_risk"
    else:
        verdict = "high_risk"

    # Extract tip
    tip = (scam_analysis.get('tip') if scam_analysis else None) or \
          "Inspect item in person before paying. Never send advance payments via JazzCash/EasyPaisa."

    return {
        "score": final_score,
        "verdict": verdict,
        "flags": combined_flags,
        "tip": tip
    }
