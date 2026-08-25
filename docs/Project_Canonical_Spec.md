# CANONICAL PROJECT SPEC — Marketplace Risk Detector

Use this exact document as context when asking any AI tool to generate architecture, workflow, code, or design for this project. Do not paraphrase or summarize it further before pasting — paste it whole so terminology stays identical across tools.

## 1. Fixed Project Identity
- **Name:** Marketplace Risk Detector
- **Event:** DoraHacks 2.0 "Vibe Coding" hackathon
- **Build deadline:** Aug 25, 2026 | **Launch/feedback phase:** Aug 25–29 | **Product Hunt launch:** Aug 29–30

## 2. Problem Statement (verbatim)
Buyers on Pakistani peer-to-peer marketplaces (OLX Pakistan, local Facebook Marketplace groups, Daraz third-party sellers) have no way to judge whether a listing is legitimate until they are already mid-conversation with the seller — by which point they have often shared contact info or been pressured into an advance payment. There is no upfront trust signal before engaging.

## 3. Solution (verbatim)
The buyer pastes a listing's text (title, description, price, category, optional seller info). The system returns a 0–100 trust score with plain-English red flags in seconds, so the buyer decides whether to engage before investing time or money — not after.

## 4. Scope Boundary — Fixed
- **Target market:** Pakistani marketplace buyers specifically (not global/generic).
- **Localization focus:** advance-payment-only demands via JazzCash/EasyPaisa, "COD not available, pay first" pressure language, Urdu-English mixed listing text, price ranges relevant to the local market.
- **Out of scope for MVP:** login/accounts, scraping listing URLs directly, payment processing, mobile app, any feature beyond the 5 listed below.

## 5. Exact MVP Feature List (5 features, fixed — do not add or remove)
1. Paste-a-listing form (title, description, price, category, optional seller info)
2. AI risk analysis tuned to Pakistani marketplace scam patterns
3. Trust score (0–100) + plain-English red-flag breakdown
4. Feedback capture (thumbs up/down — "was this accurate?")
5. Share/result card (for Product Hunt & social sharing)

## 6. Fixed Tech Stack — use exactly this, no substitutions
- **Frontend:** React + Tailwind CSS
- **Backend:** Python + Flask (single app)
- **AI/LLM:** Google GenAI SDK (`gemini-3.6-flash`) with structured output schema & fallback rules
- **Database:** MongoDB Atlas, free tier (M0) with local mock fallback
- **Deployment:** Vercel (frontend) + Render/Railway/Vercel (Flask backend)
- **Shared data contract:** every score response returns this exact JSON shape:
```json
{
  "score": 0,
  "verdict": "low_risk | medium_risk | high_risk",
  "flags": ["string", "..."],
  "tip": "string"
}
```

## 7. Fixed Role Division — use exactly these labels, always in this order
- **Person A — Buyer Experience:** owns the full UI journey — the paste-form and the results/feedback screens. Primarily frontend, with the light backend endpoints (`/api/submit`, `/api/feedback`) that serve those screens.
- **Person B — Price Intelligence:** owns the market price-reference data and the price-deviation calculation (is this listing's price abnormal for its category). Backend only.
- **Person C — Scam Detection:** owns the Gemini LLM integration, scam-pattern prompt logic, and the feedback loop that improves detection over time. Backend + AI.

## 8. Fixed Data Flow
1. Buyer submits listing via Person A's form
2. Request splits into two parallel checks: Person B's price-deviation calculation, and Person C's Gemini-based scam-pattern analysis
3. Both results merge into one combined trust score + flag list (matches the JSON contract in section 6)
4. Person A's results screen displays the combined output to the buyer
5. Buyer submits feedback (thumbs up/down), which feeds back into Person C's detection logic

## 9. Named Competitors
Scamnova, DealFlip AI, WatchdogAI/Spottable — all solve the generic "paste and score" mechanic for Western marketplaces. This project's differentiation is the Pakistani-market localization in section 4, not the score mechanic itself.
