"""
Feedback loop processing for Scam Detection (Person C Scope)
"""

def get_recent_correction_hints(limit: int = 5) -> str:
    """
    Attempts to read up to `limit` most recent submissions where
    feedback.was_accurate is False and scam_analysis exists, from the
    `submissions` collection. Returns a short plain-text summary of what
    was previously misjudged, for injection into the prompt as extra
    context. Must return "" (not raise) if:
      - db.client.get_db cannot be imported
      - get_db() returns None
      - the query fails for any reason
    Never let this function block or crash scam detection.
    """
    try:
        # Lazy imports at function level
        from db.client import get_db
        
        db = get_db()
        if db is None:
            return ""
            
        # Retrieve documents where feedback.was_accurate is False and scam_analysis exists
        cursor = db.submissions.find(
            {
                "feedback.was_accurate": False,
                "scam_analysis": {"$exists": True}
            }
        ).sort("created_at", -1).limit(limit)
        
        hints = []
        for doc in cursor:
            # Safely extract listing inputs
            inp = doc.get("input", {})
            title = inp.get("title", "N/A")
            desc = inp.get("description", "N/A")
            
            # Safely extract scam analysis details
            scam_analysis = doc.get("scam_analysis", {})
            score = scam_analysis.get("scam_score", "N/A")
            flags = scam_analysis.get("scam_flags", [])
            tip = scam_analysis.get("tip", "N/A")
            
            hints.append(
                f"- Title: {title}\n"
                f"  Description: {desc}\n"
                f"  Our Assessment: Score={score}, Flags={flags}, Tip='{tip}'\n"
                f"  Feedback: User flagged this assessment as inaccurate."
            )
            
        if not hints:
            return ""
            
        return "\n".join(hints)
        
    except Exception:
        # Never let this function block or crash scam detection
        return ""
