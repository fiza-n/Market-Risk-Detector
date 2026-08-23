import uuid
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from merge.combine import combine_results

submit_bp = Blueprint('submit', __name__)

def _fallback_scam_analysis(title, description, price, seller_info):
    text = f"{title} {description} {seller_info or ''}".lower()
    flags = []
    scam_score = 0

    if any(kw in text for kw in ['advance', 'jazzcash', 'easypaisa', 'pay first', 'token money', 'bank transfer']):
        flags.push("Advance payment pressure detected via mobile wallet / bank transfer before delivery.") if hasattr(flags, 'push') else flags.append("Advance payment pressure detected via mobile wallet / bank transfer before delivery.")
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

def _fallback_price_analysis(price, category):
    # Basic sanity check fallback
    price_val = float(price) if price else 0
    flags = []
    deviation_score = 0

    if category == "Mobile Phones" and price_val > 0 and price_val < 30000:
        flags.append("Price is significantly below average market reference for smartphones.")
        deviation_score = 30

    return {
        "price_deviation_score": deviation_score,
        "price_flags": flags,
        "category_reference_range": {"min": 30000, "max": 250000}
    }

@submit_bp.route('/submit', methods=['POST'])
def submit_listing():
    data = request.get_json() or {}

    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    price = data.get('price', 0)
    category = data.get('category', 'Mobile Phones')
    seller_info = data.get('seller_info', None)

    if not title or not description:
        return jsonify({"error": "Title and description are required fields"}), 400

    submission_id = str(uuid.uuid4())
    submitted_at = datetime.now(timezone.utc).isoformat()

    # Attempt to import Person B & Person C logic dynamically if available
    price_analysis = None
    scam_analysis = None

    try:
        from price_intelligence.deviation import calculate_price_deviation
        price_analysis = calculate_price_deviation(price, category)
    except Exception:
        price_analysis = _fallback_price_analysis(price, category)

    try:
        from scam_detection.groq_client import analyze_scam_patterns
        scam_analysis = analyze_scam_patterns(title, description, seller_info)
    except Exception:
        scam_analysis = _fallback_scam_analysis(title, description, price, seller_info)

    # Combine into Object #4
    result = combine_results(price_analysis, scam_analysis)
    result['submission_id'] = submission_id

    # Optional Mongo DB persistence if DB client is configured
    try:
        from db.client import get_db
        db = get_db()
        if db is not None:
            db.submissions.insert_one({
                "_id": submission_id,
                "input": {
                    "title": title,
                    "description": description,
                    "price": price,
                    "category": category,
                    "seller_info": seller_info,
                    "submitted_at": submitted_at
                },
                "price_analysis": price_analysis,
                "scam_analysis": scam_analysis,
                "result": result,
                "feedback": None,
                "created_at": submitted_at
            })
    except Exception as e:
        # Non-blocking log if DB is unavailable
        pass

    return jsonify(result), 200
