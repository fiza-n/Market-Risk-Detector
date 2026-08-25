import logging
import uuid
from datetime import datetime, timezone

from flask import Blueprint, request, jsonify

from merge.combine import combine_results
from price_intelligence.deviation import analyze_price

logger = logging.getLogger(__name__)

submit_bp = Blueprint('submit', __name__)


def _fallback_scam_analysis(title, description, price, seller_info):
    text = f"{title} {description} {seller_info or ''}".lower()
    flags = []
    scam_score = 0

    if any(kw in text for kw in ['advance', 'jazzcash', 'easypaisa', 'pay first', 'token money', 'bank transfer']):
        flags.append("Advance payment pressure detected via mobile wallet / bank transfer before delivery.")
        scam_score += 45

    if any(kw in text for kw in ['cod not available', 'no cod', 'delivery only']):
        flags.append("Seller refuses Cash on Delivery (COD) or in-person verification.")
        scam_score += 25

    if any(kw in text for kw in ['urgent sale', 'leaving country', 'shifting abroad', 'emergency']):
        flags.append("Time pressure language used to rush payment without verification.")
        scam_score += 20

    if not flags:
        flags.append("Pattern scan complete: No high-risk scam indicators found.")

    tip = "Always insist on inspecting the item in person before making any payment."
    if scam_score > 40:
        tip = "CRITICAL: Do NOT send advance money via JazzCash or EasyPaisa. Require in-person inspection or trusted COD."

    return {
        "scam_score": min(100, scam_score),
        "scam_flags": flags,
        "tip": tip
    }


@submit_bp.route('/submit', methods=['POST'])
def submit_listing():
    data = request.get_json() or {}
    client_session_id = data.get('client_session_id')

    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    price = data.get('price', 0)
    category = data.get('category', 'Mobile Phones')
    seller_info = data.get('seller_info', None)

    if not title or not description:
        return jsonify({"error": "Title and description are required fields"}), 400

    submission_id = str(uuid.uuid4())
    submitted_at = datetime.now(timezone.utc).isoformat()

    # Person B's price-deviation logic. No fallback needed here — this is
    # deterministic local code (no external API call), so if it throws,
    # that's a real bug worth seeing, not something to paper over.
    price_analysis = analyze_price(price, category)

    # Person C's scam-detection logic depends on an external LLM call, so a
    # fallback is legitimate here — but log it, don't swallow it silently.
    try:
        from scam_detection.groq_client import analyze_scam_patterns
        scam_analysis = analyze_scam_patterns(title, description, seller_info)
    except Exception:
        logger.exception("Scam detection failed for submission %s, using fallback", submission_id)
        scam_analysis = _fallback_scam_analysis(title, description, price, seller_info)

    # Combine into Object #4
    result = combine_results(price_analysis, scam_analysis)
    result['submission_id'] = submission_id

    # Optional Mongo DB persistence if DB client is configured
    try:
        from db import db as mongo_db
        if mongo_db is not None:
            mongo_db.submissions.insert_one({
                "_id": submission_id,
                "input": {
                    "title": title,
                    "description": description,
                    "price": price,
                    "category": category,
                    "seller_info": seller_info,
                    "client_session_id": client_session_id,
                    "submitted_at": submitted_at
                },
                "price_analysis": price_analysis,
                "scam_analysis": scam_analysis,
                "result": result,
                "feedback": None,
                "created_at": submitted_at
            })
    except Exception:
        logger.exception("Failed to persist submission %s to MongoDB", submission_id)

    return jsonify(result), 200