# Marketplace Risk Detector

> **Pause before you pay.**  
> An upfront AI-powered trust signal for buyers on Pakistani peer-to-peer marketplaces before investing time, sharing contact info, or sending advance money.

Built for **DoraHacks 2.0 "Vibe Coding"** Hackathon.  
Target Market: **Pakistani P2P Marketplace Buyers** (OLX Pakistan, Facebook Marketplace groups, Daraz third-party sellers).

---

## 📌 Problem Statement

Buyers on Pakistani peer-to-peer marketplaces (OLX Pakistan, local Facebook Marketplace groups, Daraz third-party sellers) have no way to judge whether a listing is legitimate until they are already mid-conversation with the seller — by which point they have often shared contact info or been pressured into an advance payment. There is no upfront trust signal before engaging.

---

## 💡 Solution

The buyer pastes a listing's text (title, description, price, category, optional seller info). The system returns a **0–100 Trust Score** with plain-English red flags in seconds, so the buyer decides whether to engage before investing time or money — not after.

---

## 🎯 5 Core MVP Features

1. **Paste-a-Listing Form:** Simple form accepting title, description, price (PKR), category, and optional seller info (with a one-click sample scam listing loader).
2. **Pakistani Scam Pattern AI Analysis:** LLM prompt engine tuned specifically to detect local fraud patterns (JazzCash/EasyPaisa advance demands, COD refusal, urgency pressure, Roman Urdu code-mixed phrasing).
3. **0–100 Trust Score & Red Flag Breakdown:** Visual gauge rendering a 0–100 score, risk verdict (`low_risk`, `medium_risk`, `high_risk`), plain-English red flags, and actionable buyer safety tips.
4. **Accuracy Feedback Capture:** Thumbs up/down voting loop ("Was this assessment accurate?") feeding user corrections back into future detection prompts.
5. **Shareable Result Card:** Formatted result card snippet easily copyable to WhatsApp, Product Hunt, or social media to help friends pause before paying.

---

## 🇵🇰 Localization Focus (Pakistani Marketplace Specifics)

Unlike generic global risk tools, **Marketplace Risk Detector** is specifically engineered for Pakistan:
- **Advance Payment Pressure:** Detects demands for "token money" or advance transfer via JazzCash, EasyPaisa, or bank transfer prior to physical inspection.
- **COD Refusal:** Flags listings explicitly disallowing Cash on Delivery or in-person verification.
- **Language & Culture:** Understood mixed Roman Urdu & Urdu phrasing (e.g., *"urgent bechna hai"*, *"advance payment hogi"*).
- **Localized Reference Pricing:** Compares asking prices against typical Pakistani market price ranges across categories.

---

## 🏗️ Architecture & Data Flow

```
[ Buyer ]
    │
    ▼
[ Person A: React Frontend (safespot.pk UI) ]
    │  POST /api/submit
    ▼
[ Person A: Flask API Endpoint ]
    ├──► [ Person B: Price Intelligence ] ---> Category Price Deviation Score (0-100)
    └──► [ Person C: Scam Detection AI ]  ---> Gemini 3.6 Scam Analysis Score (0-100)
    │
    ▼
[ Merging Engine (merge/combine.py) ]
    │  Score = 100 - (Price_Score * 0.4 + Scam_Score * 0.6)
    ▼
[ Object #4 JSON Contract Response ] ---> Rendered on Results Screen
```

---

## 🛠️ Tech Stack

- **Frontend:** React 19 + Vite 6 + Tailwind CSS + Lucide Icons
- **Backend:** Python 3.14 + Flask + Flask-CORS
- **AI Engine:** Google GenAI SDK (`gemini-3.6-flash`) with structured JSON schema
- **Database:** MongoDB Atlas (M0 Free Tier) with local mock fallback
- **Testing:** pytest (Backend unit & integration tests)

---

## 👥 Team & Roles

| Role | Name | Responsibilities |
|---|---|---|
| **Person A — Buyer Experience** | **Ummama** | Full UI journey (paste-form, results screen, feedback buttons, share card). Frontend + Flask route handlers (`/api/submit`, `/api/feedback`). |
| **Person B — Price Intelligence** | **Fiza** | Category market price reference data, price deviation calculation, MongoDB initialization & schema definitions. |
| **Person C — Scam Detection** | **Javeria** | Gemini 3.6 Flash integration, Pakistani scam prompt engineering, feedback loop context injection. |

---

## 📄 Shared API Contract (Object #4)

Every `/api/submit` request returns this exact JSON response:

```json
{
  "submission_id": "8f3b2a1c-9d4e-4f7a-8b1c-2d3e4f5a6b7c",
  "score": 42,
  "verdict": "medium_risk",
  "flags": [
    "Advance payment pressure detected via mobile wallet / bank transfer before delivery.",
    "Seller refuses Cash on Delivery (COD) or in-person verification."
  ],
  "tip": "CRITICAL: Do NOT send advance money via JazzCash or EasyPaisa. Require in-person inspection or trusted COD."
}
```

---

## 🛡️ Resilience & Offline Fallback Architecture

The system is built to be resilient in all network environments:
- **Offline DB:** If MongoDB is offline, `db.py` handles timeouts (2s limit), falling back to in-memory `DEFAULT_CATEGORIES`.
- **Offline LLM:** If the Gemini API fails, `routes/submit.py` falls back to regex pattern scanning (`_fallback_scam_analysis`).
- **Offline Backend:** If the backend is down, the frontend (`client.js`) transparently switches to `mockApi.js`.

---

## 🚀 Quick Start Guide

### Prerequisites
- Node.js (v18+)
- Python (3.10+)

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```
Backend runs on `http://localhost:5000`.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:3000`.

---

## 🧪 Running Tests

Execute all 20 unit and integration tests across all backend modules:

```bash
cd backend
python -m pytest tests/ -v
```

---

## 📚 Documentation Reference

Full specifications and data schemas are located in `/docs`:
- [`Project_Canonical_Spec.md`](docs/Project_Canonical_Spec.md) — Ground-truth project scope, stack rules, and role divisions.
- [`Shared_Data_Contract.md`](docs/Shared_Data_Contract.md) — Complete object contracts, MongoDB collection schemas, and field definitions.
- [`Project-Structure.md`](Project-Structure.md) — Comprehensive repository directory layout & file responsibilities.