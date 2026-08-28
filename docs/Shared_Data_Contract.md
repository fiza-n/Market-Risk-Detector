# SHARED DATA CONTRACT — Marketplace Risk Detector

Companion doc to `Project_Canonical_Spec.md`. Read that first for scope/roles/deadlines — this doc covers **data shapes**: what objects exist, who owns each one, and what MongoDB stores. All team members work from this exact document so field names never drift between frontend, Person B's code, and Person C's code.

---

## 1. The ID That Ties Everything Together

There is no login/accounts in this MVP (spec §4). Instead:

- **`submission_id`** — a UUID generated server-side the moment a buyer submits the paste-form. Every object below (input, price analysis, scam analysis, merged result, feedback) carries this same ID. Think of it as the spine of one "listing check."
- **`client_session_id`** — a throwaway ID the frontend generates (`crypto.randomUUID()` stored in localStorage) purely so the UI can track anonymous buyer sessions.

---

## 2. Object #1 — Listing Input
**Owner: Person A** (paste-form + `/api/submit` endpoint)

```json
{
  "submission_id": "string (UUID, server-generated)",
  "title": "string",
  "description": "string",
  "price": "number (PKR)",
  "category": "string (Mobile Phones | Electronics | Vehicles | Furniture | Fashion | Property/Rent | Other)",
  "seller_info": "string | null",
  "client_session_id": "string | null",
  "submitted_at": "ISO 8601 timestamp"
}
```

---

## 3. Object #2 — Price Intelligence Result (internal)
**Owner: Person B** (`price_intelligence/deviation.py`). Backend-only, feeds the merge step.

```json
{
  "price_deviation_score": "number 0-100 (higher = more suspicious/underpriced)",
  "price_flags": ["string", "..."],
  "category_reference_range": { "min": "number", "max": "number" }
}
```

---

## 4. Object #3 — Scam Detection Result (internal)
**Owner: Person C** (`scam_detection/groq_client.py`). Uses Google GenAI SDK (`gemini-3.6-flash`). Internal.

```json
{
  "scam_score": "number 0-100 (higher = more suspicious)",
  "scam_flags": ["string", "..."],
  "tip": "string (plain-English advice for the buyer)",
  "raw_llm_response": "string (debug/logging only — never sent to frontend)"
}
```

---

## 5. Object #4 — Final Combined Result (Fixed Spec §6 Contract)
This is the **only** shape Person A's frontend needs to render the results screen and share card.

```json
{
  "submission_id": "string (UUID)",
  "score": "number 0-100 (100 = highest trust, 0 = highest risk)",
  "verdict": "low_risk | medium_risk | high_risk",
  "flags": ["string", "..."],
  "tip": "string"
}
```

---

## 6. Object #5 — Feedback
**Owner: Person A** (thumbs up/down UI + `/api/feedback` endpoint), feeds Person C's feedback loop (`scam_detection/feedback_loop.py`).

```json
{
  "submission_id": "string",
  "was_accurate": "boolean",
  "submitted_at": "ISO 8601 timestamp"
}
```

---

## 7. Standardized Merge Logic (`merge/combine.py`)

Formula for combined trust score and verdict:
```python
risk_penalty = round(price_deviation_score * 0.4 + scam_score * 0.6)
final_score = max(0, min(100, 100 - risk_penalty))

verdict = "low_risk"    if final_score >= 70
          "medium_risk" if final_score >= 40
          "high_risk"   otherwise
```

---

## 8. Category Enum
Fixed set used across frontend dropdown, price reference data, and scam analysis:
`Mobile Phones | Electronics | Vehicles | Furniture | Fashion | Property/Rent | Other`

---

## 9. MongoDB Atlas (M0 free tier) Schema & Fallback Architecture

### Collection: `submissions`
```json
{
  "_id": "submission_id",
  "input": {
    "title": "...",
    "description": "...",
    "price": 0,
    "category": "...",
    "seller_info": null,
    "client_session_id": "...",
    "submitted_at": "ISO 8601"
  },
  "price_analysis": { ... },
  "scam_analysis": { ... },
  "result": { ... },
  "feedback": { "was_accurate": true, "submitted_at": "ISO 8601" },
  "created_at": "ISO 8601"
}
```

### Collection: `category_price_references`
```json
{
  "category": "string",
  "typical_min_price": "number",
  "typical_max_price": "number",
  "updated_at": "ISO 8601"
}
```

### Offline & Resilience Architecture
1. **Database Fallback:** If MongoDB is offline or unreachable, `db.py` handles exceptions gracefully (`db = None`), `reference_data.py` uses in-memory default category ranges, and submission endpoints return results without throwing 500 errors.
2. **LLM Fallback:** If the Gemini API call fails or times out, `routes/submit.py` falls back to regex-based Pakistani scam pattern detection (`_fallback_scam_analysis`).
3. **Frontend Fallback:** If the backend service is offline, `frontend/src/api/client.js` uses `mockApi.js` to ensure the UI remains fully functional.
