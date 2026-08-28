# PROJECT STRUCTURE & MODULE ARCHITECTURE

This document defines the layout, responsibilities, and ownership of every module in the **Marketplace Risk Detector** codebase.

---

## Overview Directory Layout

```
Market-Risk-Detector/
├── docs/                        # Architecture specs & shared data contracts
│   ├── Project_Canonical_Spec.md  # Ground-truth project spec (scope, stack, roles)
│   └── Shared_Data_Contract.md    # Shared API contracts & MongoDB schemas
│
├── frontend/                    # React + Tailwind CSS client application (Owner: Person A - Ummama)
│   ├── index.html               # Entry HTML with meta description & Google fonts
│   ├── vercel.json              # Vercel deployment rewrite rules
│   ├── vite.config.js           # Vite server, port, Tailwind plugin & API proxy config
│   └── src/
│       ├── App.jsx              # Main router & top layout header/footer navigation
│       ├── index.css            # Design system tokens & Tailwind CSS imports
│       ├── main.jsx             # React entry point
│       ├── api/
│       │   ├── client.js        # Production fetch wrapper with backend fallback
│       │   └── mockApi.js       # Offline mock risk analyzer matching Object #4 shape
│       ├── components/
│       │   ├── ListingForm.jsx  # Paste-a-listing input form + sample scam loader
│       │   ├── ResultCard.jsx   # 0–100 Trust Score gauge & plain-English red flags
│       │   ├── FeedbackButtons.jsx # Thumbs up/down accuracy voting component
│       │   └── ShareCard.jsx    # Shareable trust signal card for Product Hunt
│       └── pages/
│           ├── HomePage.jsx     # Landing page with value proposition & hero section
│           ├── SubmitPage.jsx   # Check-a-listing wrapper page
│           └── ResultPage.jsx   # Risk assessment report page
│
├── backend/                     # Python + Flask REST API (Owners: Person A, B, C)
│   ├── app.py                   # Flask app factory, CORS configuration, health endpoint
│   ├── config.py                # Environment variable loader (API keys, Mongo URI, Port)
│   ├── constants.py             # Shared constants & category default definitions
│   ├── db.py                    # Safe MongoDB connection initializer (Owner: Person B - Fiza)
│   ├── requirements.txt         # Production Python dependencies
│   │
│   ├── routes/                  # API HTTP Blueprints (Owner: Person A - Ummama)
│   │   ├── submit.py            # POST /api/submit — runs parallel checks & merges results
│   │   ├── feedback.py          # POST /api/feedback — records accuracy votes to DB
│   │   └── meta.py              # GET /api/meta/categories — serves category list
│   │
│   ├── price_intelligence/      # Price Deviation Analysis (Owner: Person B - Fiza)
│   │   ├── deviation.py         # Category market price comparison & scoring logic
│   │   └── reference_data.py    # Database lookup with in-memory default category fallback
│   │
│   ├── scam_detection/          # AI Scam Pattern Detection (Owner: Person C - Javeria)
│   │   ├── groq_client.py       # Google GenAI SDK integration with gemini-3.6-flash
│   │   ├── prompt.py            # Pakistani marketplace scam system instruction & prompts
│   │   └── feedback_loop.py     # Pulls past inaccurate votes into context window
│   │
│   ├── merge/                   # Result Merging Engine (Shared / Person A)
│   │   └── combine.py           # Merges price score & scam score into Object #4 contract
│   │
│   └── tests/                   # Automated Unit & Integration Test Suite
│       ├── test_merge.py        # Validates score weighting, verdict thresholds, flag deduplication
│       ├── test_price_intelligence.py # Validates price deviation calculations & category ranges
│       └── test_scam_detection.py     # Validates scam LLM schema, fallback, and feedback loop
│
└── README.md                    # Main project documentation, problem statement & setup guide
```

---

## Component Roles & Responsibilities

| Directory / File | Role Owner | Primary Purpose |
|---|---|---|
| `docs/` | Shared | Canonical source of truth for features, tech stack, data contracts, and scope boundaries. |
| `frontend/` | Person A (Ummama) | Interactive web interface for Pakistani buyers to check listings, view trust scores, submit feedback, and share cards. |
| `backend/routes/` | Person A (Ummama) | REST endpoints that orchestrate request handling, trigger price + scam analysis, and return Object #4 contract. |
| `backend/price_intelligence/` | Person B (Fiza) | Deterministic local analysis comparing asking price against typical category ranges to compute price deviation scores. |
| `backend/scam_detection/` | Person C (Javeria) | AI analysis using Gemini 3.6 Flash to identify advance payment, JazzCash/EasyPaisa, urgency, and Roman Urdu scam patterns. |
| `backend/db.py` | Person B (Fiza) | Safe MongoDB connection initializer with 2-second timeout and offline graceful fallback. |
| `backend/merge/combine.py` | Shared | Combines price penalty (40%) and scam penalty (60%) into a 0–100 Trust Score and verdict. |
| `backend/tests/` | Shared | Test suite ensuring 100% test coverage across merge logic, price intelligence, and scam pattern analysis. |
