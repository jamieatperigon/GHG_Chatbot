# GHG Emissions Chatbot System

A scalable, AI-powered chatbot for recording and calculating greenhouse gas (GHG) emissions — with support for transport, heating, electricity, and more. Designed for small businesses and consultancies needing accurate Scope 1, 2, and 3 reporting.

---

## 🧠 Overview

This chatbot runs via **Microsoft Teams** (or another chat interface) and uses **FastAPI + OpenAI GPT** to:

- Collect travel/emissions info from users in natural language
- Retrieve conversion factors from the UK Government's **DEFRA dataset**
- Log transport and emissions data in a structured database
- Prompt for missing info rather than guessing
- Prepare robust records for annual GHG reporting

---

## ⚙️ Tech Stack

| Component       | Tech                        |
|----------------|-----------------------------|
| Bot Interface   | Microsoft Teams (via Bot Framework or webhook) |
| Backend API     | FastAPI (Python)            |
| AI Reasoning    | OpenAI API (e.g. GPT-4o)    |
| Database        | SQLite                      |
| Hosting         | Railway / Render / Replit (or local dev) |
| (Optional) Geocoding | Google Maps, OpenCage, or OSRM |

---

## 🏗️ System Architecture

### 1. **User → Teams Chat**
Users type natural-language logs:
> "Drove to the office today in the hybrid car"

Teams forwards this message to your FastAPI webhook.

---

### 2. **FastAPI Backend**

Handles:
- `/message` → Process user input via GPT
- `/profile/{user_id}` → Create or update user info
- `/logs` → Store structured emissions data

---

### 3. **Profile System (SQLite)**

Each user has:
- Home postcode
- Office postcode
- 1+ registered vehicles (with DEFRA factor ID)
- Optional heating/electricity setup

This avoids repeating information every time.

---

### 4. **DEFRA Conversion Factor Table**

Stored as a normalized table with:
- `factor_id`
- `level_1` → `level_4` hierarchy
- `type`: Direct / WTT / T&D
- `unit`, `conversion_factor`, `scope`

Covers **all transport, heating, electricity, and more** from the official 2025 DEFRA dataset.

---

### 5. **Emission Logging**

Each message results in a new `emission_logs` entry:

| Field                | Example                              |
|---------------------|--------------------------------------|
| `user_id`           | jamie                                |
| `date`              | 2025-07-03                           |
| `transport_mode`    | Petrol car                           |
| `distance_km`       | 43.2                                 |
| `conversion_factor` | 0.18043                              |
| `wtt_factor`        | 0.04631                              |
| `emissions_total`   | 9.78 kg CO₂e                         |
| `scope`             | 3.6 (Business travel)                |

AI will:
- Prompt for distance or infer from locations
- Prompt for vehicle or use profile
- **Never hallucinate** emission factors

---

## 🚗 Supported Transport Modes

The system supports **all transport modes** published by DEFRA, including:

- 🚘 Cars (petrol, diesel, hybrid, EV)
- 🚌 Buses
- 🚆 Rail (national, international)
- 🚇 Tube, tram, DLR
- ✈️ Flights (short/long haul, domestic)
- 🚢 Ferries and watercraft
- 🚕 Taxis, ride-share
- 🚶 Walking & cycling (zero emissions)
- 🛸 Helicopters, private jets, etc. (with manual lookup)

---

## 📊 Reporting (Planned)

You can generate summary tables like:

```
Greenhouse Gas Emissions

Emissions Source                 | Scope | 2025 | 2024 | 2023
--------------------------------------------------------------
Business Travel                  | 3.6   | 2.0  | 1.1  | 6.5
Employee Commuting & Homeworking| 3.7   | 0.3  | 0.4  | 0.3
Heating of Home Office          | 1     | 1.9  | 1.8  | 2.0
Purchased Electricity           | 2     | 0.0  | 0.2  | 0.1
Total All Scopes                | 1–3   | 4.2  | 3.5  | 8.9
```

And intensity metrics:
- Emissions per £m
- Target tracking

---

## 🔐 Privacy & Security

All emissions data is user-specific and stored securely in the SQLite database. Designed for eventual cloud migration (e.g. PostgreSQL on Supabase).

---

## ✅ Getting Started

```bash
# Clone this repo
git clone https://github.com/your-org/ghg-chatbot.git
cd ghg-chatbot

# Install dependencies
pip install -r requirements.txt

# Run the app locally
uvicorn main:app --reload
```

---

## 📦 Folder Structure

```
ghg-chatbot/
├── main.py              # FastAPI app
├── db.py                # SQLite DB setup + utilities
├── prompts.py           # GPT system prompt
├── defra_loader.py      # Import DEFRA spreadsheet
├── conversion_factors.db# Preloaded SQLite DB
├── requirements.txt
└── README.md
```

---

## 🛣️ Roadmap

- [x] Full DEFRA transport dataset
- [x] Profile-aware AI prompt
- [x] Multi-vehicle support
- [ ] Add heating & electricity
- [ ] Dashboard/reporting UI
- [ ] Supabase/Postgres migration

---

## 👤 Created by

Jamie Thomson  
Perigon Partners  
[OpenAI-powered GHG systems for ESG](https://perigonpartners.co.uk)