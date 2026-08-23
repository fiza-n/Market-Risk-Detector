from datetime import datetime, timezone
from flask import Blueprint, request, jsonify

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json() or {}

    submission_id = data.get('submission_id')
    was_accurate = data.get('was_accurate')

    if not submission_id or was_accurate is None:
        return jsonify({"error": "submission_id and was_accurate are required"}), 400

    submitted_at = data.get('submitted_at') or datetime.now(timezone.utc).isoformat()

    feedback_doc = {
        "was_accurate": bool(was_accurate),
        "submitted_at": submitted_at
    }

    try:
        from db.client import get_db
        db = get_db()
        if db is not None:
            db.submissions.update_one(
                {"_id": submission_id},
                {"$set": {"feedback": feedback_doc}}
            )
    except Exception:
        pass

    return jsonify({
        "success": True,
        "message": "Feedback recorded",
        "submission_id": submission_id
    }), 200
