# Holly — AI Leasing Assistant

> Built as a working alternative to a $1.08M/year third-party vendor. One engineer. No budget. No mandate.

---

## The Problem

The company was spending **$90,000/month across 34 properties** on [EliseAI](https://www.eliseai.com/) — a third-party AI leasing assistant. The service worked, but it meant:

- No internal ownership of conversation data
- No ability to customize responses per property
- Full dependency on an external vendor roadmap
- A fixed cost that scaled with the portfolio regardless of usage

I built Holly to answer a simple question: *could one person replicate the core of this product using open APIs, and bring that spend in-house?*

The answer was yes. The prototype worked end-to-end. It didn't ship — not because of a technical failure, but because leadership couldn't move past an existing vendor contract. That's documented in the [Why It Didn't Ship](#why-it-didnt-ship) section below.

---

## What It Does

Holly is a property-aware AI leasing assistant that answers prospect questions in real time using **live data** — not static FAQs.

- A prospect asks about availability at a specific property
- Holly fuzzy-matches the property name to the database
- Pulls live unit types, pricing, and availability from the Entrata API
- Responds conversationally with accurate, current information
- Logs the full conversation to Supabase for audit and reporting

Each property gets its own configuration: assistant name, tone, and response style. The AI doesn't hallucinate availability — it reads from a live sync.

---

## Architecture

```
Entrata Partner API
        │
        ▼
  Sync Scripts (Python)          ← getproperties.py, getunittypes.py,
        │                           entratatosupabase.py, getLeads.py
        ▼
  Supabase (PostgreSQL)          ← Single source of truth
        │                           properties, unit_types, leads,
        │                           conversation_logs
        ▼
  AI Response Layer (Python)     ← GPT-4.1 + custom prompt system
        │                           Intent parsing, fuzzy property matching,
        │                           proration-aware pricing logic
        ▼
  Frontend (React + Tailwind)    ← Property selector, chat UI
  + Gradio Prototype             ← Functional demo, validated end-to-end
```

**Key engineering decisions:**
- Separated the **data sync layer** from the **AI response layer** — Entrata flows into Supabase on a schedule; the AI reads from Supabase, never directly from the API. This makes the AI fast and the sync independently maintainable.
- **Fuzzy matching** resolves informal property name inputs (`"The Scarlet"` → `"5222 The Scarlet Apartments"`) using configurable confidence thresholds — no hardcoded lookups.
- **Custom intent parser** handles natural language unit queries (`"two bedroom"`, `"3x2"`, `"studio"`) and maps them to structured database queries using regex-based extraction.
- **Upsert logic** prevents duplicate records on re-sync — properties, unit types, and leads are idempotently refreshed.
- **Full conversation logging** to Supabase and Excel for audit trail and downstream reporting.

---

## Tech Stack

| Layer | Tools |
|---|---|
| AI Engine | OpenAI GPT-4.1, custom prompt system |
| Backend | Python, Node.js |
| Database | Supabase (PostgreSQL) |
| Property Data | Entrata Partner API |
| Frontend | React, Tailwind CSS |
| Prototype UI | Gradio |
| Storage | AWS S3 |
| Config | python-dotenv |
| Planned | Twilio (voice/SMS), AWS Lambda |

---

## Key Modules

| File | What It Does |
|---|---|
| `assistant.py` | Core AI response engine — GPT-4.1 integration, prompt system, property context injection |
| `chatbot.py` | Conversation loop, intent routing, session management |
| `entratatosupabase.py` | Syncs property and unit data from Entrata API into Supabase |
| `getLeads.py` | Pulls leads by property/date range from Entrata, inserts structured records |
| `getproperties.py` | Fetches and normalizes property list from Entrata |
| `getunittypes.py` | Fetches unit type/pricing/availability per property |
| `utils.py` | Fuzzy matching engine, intent parser, shared helpers |
| `mainSupabase.py` | Database client and query layer |

---

## Local Setup

**Prerequisites:** Python 3.9+, Node.js 18+, Supabase project, Entrata API credentials, OpenAI API key

```bash
# Clone
git clone https://github.com/Jacosta327/AI-Assistant.git
cd AI-Assistant

# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend && npm install

# Environment variables — create .env in root and frontend/
```

**.env (root)**
```ini
OPENAI_API_KEY=your-openai-key
ENTRATA_BASE_URL=your-entrata-url
ENTRATA_USERNAME=your-entrata-username
ENTRATA_PASSWORD=your-entrata-password
SUPABASE_URL=your-supabase-project-url
SUPABASE_SERVICE_KEY=your-supabase-service-key
```

```bash
# Sync properties from Entrata into Supabase
python backend/scripts/getproperties.py
python backend/scripts/getunittypes.py
python backend/scripts/entratatosupabase.py

# Run the assistant
python backend/assistant.py

# Run frontend
cd frontend && npm run dev
```

---

## Project Status

| Component | Status |
|---|---|
| Entrata API integration (live property/unit data) | ✅ Complete |
| Supabase backend + upsert sync | ✅ Complete |
| GPT-4.1 AI response engine | ✅ Complete |
| Fuzzy property matching | ✅ Complete |
| Intent parser (bed/bath extraction) | ✅ Complete |
| Lead ingestion pipeline | ✅ Complete |
| Full conversation logging | ✅ Complete |
| Gradio prototype (end-to-end validated) | ✅ Complete |
| React + Tailwind frontend | 🚧 In progress |
| Admin panel (per-property editing) | 🚧 Planned |
| Twilio voice/SMS integration | 🚧 Planned |
| Resident vs. prospect logic branching | 🚧 Planned |
| Maintenance request routing | 🚧 Planned |

---

## Why It Didn't Ship

The prototype worked. The system answered leasing questions accurately using live data, logged every conversation, and was running end-to-end before the project was paused.

It didn't ship because the company was already locked into an EliseAI contract and leadership viewed a self-built alternative as too risky to evaluate seriously — not because of technical concerns, but organizational ones. There was no internal appetite to champion a vendor replacement, even with a working prototype.

This is documented honestly because it's relevant context. The technical barrier was cleared. The barrier that stopped it was a business decision, not an engineering failure.

---

## What This Demonstrates

- Ability to **identify a seven-figure cost problem** without being asked
- **Independently architecting** a full-stack AI product (data pipeline → AI layer → frontend)
- Working with **live production APIs** (Entrata Partner API) for real data sync
- Building for **non-technical operators** — configurable, auditable, maintainable
- Honest engineering judgment — knowing what's done, what's planned, and why things stopped

---

## Roadmap (if continued)

- Twilio voice integration — after-hours call answering
- Maintenance ticket routing directly into Entrata
- Analytics dashboard for lead/resident interaction trends
- RAG (Retrieval Augmented Generation) for fact-checked responses against property documents
- Multi-industry architecture (beyond property management)

---

## License

© 2025 Jesus Acosta. All rights reserved. This project is proprietary.

*Note: Data files and API credentials have been excluded from this repository. All property, unit, and lead data shown in development was from a live environment and has been removed prior to publication.*
