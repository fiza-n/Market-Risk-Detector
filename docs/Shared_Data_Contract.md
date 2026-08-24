# SHARED DATA CONTRACT — Marketplace Risk Detector

Companion doc to `Project_Canonical_Spec.md`. Read that first for scope/roles/deadlines — this doc only covers **data shapes**: what objects exist, who owns each one, and what MongoDB actually stores. All three of you should work from this exact document so field names never drift between frontend, Person B's code, and Person C's code.

Two things below are **not fixed by the canonical spec** — they're my best-guess defaults, flagged clearly. Confirm them as a team before writing code; changing a field name after Day 2 is expensive.

---

## 1. The One ID That Ties Everything Together

There's no login/accounts in this MVP (spec §4), so there's no `user_id`. Instead:

- **`submission_id`** — a UUID generated server-side the moment a buyer submits the paste-form. Every object below (input, price analysis, scam analysis, merged result, feedback) carries this same ID. Think of it as the spine of one "listing check."
- **`client_session_id`** *(optional, my suggestion)* — a throwaway ID the frontend generates (e.g. `crypto.randomUUID()` kept in memory/localStorage) purely so the UI can say "here's your last result" during the session. Not part of the DB contract, not required — drop it if it adds friction.

---

## 2. Object #1 — Listing Input
**Owner: Person A** (paste-form + the endpoint that receives it)

```json
{
  "submission_id": "string (UUID, server-generated)",
  "title": "string",
  "description": "string",
  "price": "number (PKR)",
  "category": "string (see §7 — enum needs team decision)",
  "seller_info": "string | null",
  "submitted_at": "ISO 8601 timestamp"
}
```

## 3. Object #2 — Price Intelligence Result (internal)
**Owner: Person B.** Backend-only, never sent directly to the buyer — it feeds the merge step.

```json
{
  "submission_id": "string",
  "price_deviation_score": "number 0-100 (higher = more suspicious)",
  "price_flags": ["string", "..."],
  "category_reference_range": { "min": "number", "max": "number" }
}
```

## 4. Object #3 — Scam Detection Result (internal)
**Owner: Person C.** Backend + Google GenAI (gemini-2.5-flash) call. Also internal.

```json
{
  "submission_id": "string",
  "scam_score": "number 0-100 (higher = more suspicious)",
  "scam_flags": ["string", "..."],
  "tip": "string (plain-English advice — becomes the final 'tip' field)",
  "raw_llm_response": "string (optional, debug/logging only — never sent to frontend)"
}
```

## 5. Object #4 — Final Result (the fixed API contract from spec §6)
This is the **only** shape Person A's frontend needs to know about for rendering. Do not deviate from this — it's fixed in the canonical spec.

```json
{
  "score": "number 0-100",
  "verdict": "low_risk | medium_risk | high_risk",
  "flags": ["string", "..."],
  "tip": "string"
}
```

## 6. Object #5 — Feedback
**Owner: Person A** (thumbs up/down UI + endpoint), feeds Person C's detection loop (spec §8 step 5).

```json
{
  "submission_id": "string",
  "was_accurate": "boolean",
  "submitted_at": "ISO 8601 timestamp"
}
```

---

## 7. ⚠️ Open Item #1: Who Owns the Merge Step?

The canonical spec's data flow (§8) says Person B's and Person C's results "merge into one combined trust score + flag list," but doesn't assign an owner. My default assumption: it belongs with **Person A's light backend endpoints** (spec §7 already gives Person A "the light backend endpoints that serve those screens") — since the results screen needs the merged object, the endpoint Person A owns is the natural place to call B's function, call C's function, and combine them.

**Confirm this as a team.** If someone disagrees, the fix is just moving one function — nothing above changes.

Suggested merge logic (placeholder — tune weights as you test):
```
final_score = 100 - round(price_deviation_score * 0.4 + scam_score * 0.6)
flags       = dedupe(price_flags + scam_flags)
verdict     = "low_risk"    if final_score >= 70
              "medium_risk" if final_score >= 40
              "high_risk"   otherwise
```

## 8. ⚠️ Open Item #2: Category Enum

The spec mentions `category` as a form field but never fixes the list — and it needs to be **identical** in Person A's dropdown, Person B's price-reference collection, and Person C's prompt logic. Suggested starter set (edit freely, just lock it before coding):

`Mobile Phones | Electronics | Vehicles | Furniture | Fashion | Property/Rent | Other`

---

## 9. MongoDB Atlas (M0 free tier) — Collections

Given the timeline, one embedded document per submission beats a normalized multi-collection design — no joins, one read gets everything for the results screen and the share card.

**Collection: `submissions`**
```json
{
  "_id": "submission_id",
  "input": { "title": "...", "description": "...", "price": 0, "category": "...", "seller_info": null, "submitted_at": "..." },
  "price_analysis": { "price_deviation_score": 0, "price_flags": [], "category_reference_range": { "min": 0, "max": 0 } },
  "scam_analysis": { "scam_score": 0, "scam_flags": [], "tip": "..." },
  "result": { "score": 0, "verdict": "...", "flags": [], "tip": "..." },
  "feedback": { "was_accurate": true, "submitted_at": "..." },
  "created_at": "ISO 8601"
}
```
`feedback` is `null` until the buyer votes.

**Collection: `category_price_references`**
Person B's seed/reference data — separate from `submissions` because it's static reference data, not per-request data, and Person B may update it independently of anyone else's code.
```json
{
  "category": "string",
  "typical_min_price": "number",
  "typical_max_price": "number",
  "updated_at": "ISO 8601"
}
```

---

## 10. Quick Reference — Who Writes What

| Data | Written by | Collection |
|---|---|---|
| `submission_id` + `input` | Person A | `submissions.input` |
| `price_analysis` | Person B | `submissions.price_analysis` |
| `scam_analysis` | Person C | `submissions.scam_analysis` |
| `result` (merged) | Person A *(see §7)* | `submissions.result` |
| `feedback` | Person A (UI+endpoint) → read by Person C | `submissions.feedback` |
| price reference data | Person B | `category_price_references` |

**Suggested endpoints (Person A owns both):**
- `POST /api/submit` → creates the `submissions` doc, calls Person B's and Person C's functions, writes `result`, returns Object #4 (§5) to the frontend.
- `POST /api/feedback` → writes `feedback` onto the existing submission by `submission_id`.

---

**How to use this:** paste this whole file (like the canonical spec) into any AI tool alongside the spec when generating code for your part — that way all three of you get identical field names even when working separately.
