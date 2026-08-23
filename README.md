# Marketplace Risk Detector

A buyer pastes a marketplace listing (title, description, price, category,
optional seller info) and gets a 0–100 trust score with plain-English red
flags in seconds — before they engage with the seller, not after.

Built for **DoraHacks 2.0 "Vibe Coding"** hackathon.
Target market: Pakistani P2P marketplace buyers (OLX Pakistan, local FB
Marketplace groups, Daraz third-party sellers).

## Timeline

- Build deadline: **Aug 25, 2026**
- Public launch / feedback phase: **Aug 25–29**
- Product Hunt launch: **Aug 29–30**

## Team

| Person | Owns | Scope |
|---|---|---|
| **Ummama** | Buyer Experience | Full UI journey — paste-form and results/feedback screens. Frontend + the light backend endpoints serving those screens. No AI work. |
| **Fiza** | Price Intelligence + Database | Market price-reference data, price-deviation calculation, MongoDB connection/schemas. Backend only. No frontend, no AI. |
| **Javeria** | Scam Detection | Groq LLM integration, scam-pattern prompt logic, feedback loop. Backend + AI. No frontend. |

## Tech Stack

- **Frontend:** React + Tailwind CSS
- **Backend:** Python + Flask (single app)
- **AI/LLM:** Groq API, Llama 3.3 70B (free tier)
- **Database:** MongoDB Atlas (free tier, M0)
- **Deployment:** Vercel (frontend) + Render or Railway (backend)

## Prerequisites

- Node.js: v22.12.0
- Python: 3.13.5
- A MongoDB Atlas connection string (shared or personal free-tier cluster)
- A Groq API key

## Setup

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Environment Variables

Copy `.env.example` to `.env` in `backend/` and fill in:

```
MONGO_URI=
GROQ_API_KEY=
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/submit` | Submits a listing, runs price + scam analysis, returns the combined result |
| `POST` | `/api/feedback` | Records a thumbs up/down for a submission |
| `GET` | `/api/meta/categories` | Returns the fixed category list, used by the frontend dropdown |

## Response Shape

Every score response returns this exact shape:

```json
{
  "score": 0,
  "verdict": "low_risk | medium_risk | high_risk",
  "flags": ["string", "..."],
  "tip": "string"
}
```

## Open Decisions

These aren't resolved in the spec — confirm as a team before/while building:

- Who owns `backend/merge/combine.py` (the score-combining logic)
- Node/Python version pins above
- Score-weighting formula (`price_deviation_score * 0.4 + scam_score * 0.6`
  is a placeholder — nobody has actually agreed price should count less
  than scam signals)

## Docs

Full spec and data contract live in `docs/`:

- `Project_Canonical_Spec.md`
- `Shared_Data_Contract.md`