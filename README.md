# TLIM — Tibia Loot & Inventory Manager
### Stage 1: Python / FastAPI / SQLite

![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)

> The first stage of a three-stage portfolio project. Stage 2 rebuilds it as a REST API in [Java / Spring Boot / PostgreSQL](https://github.com/calgadev/tlim-java), and Stage 3 puts a [React / TypeScript frontend](https://github.com/calgadev/tlim-frontend) on top of that API.

---

## What is TLIM?

TLIM is a personal portfolio project built to solve real problems faced by players of the MMORPG [Tibia](https://www.tibia.com):

- **What should I do with my loot after a hunt?** Keep it, sell to an NPC, or list on the market?
- **Where should I grind?** Which hunting spots actually generate the most value over time?

Stage 1 proves the concept with a working MVP: a server-side rendered web application that classifies loot, calculates passive gold, and stores hunt history per character for future comparison.

---

## Project Roadmap

| Stage | Stack | Repository | Status |
|---|---|---|---|
| Stage 1 — Backend + Server-side UI | Python 3.12 · FastAPI · SQLAlchemy 2.0 · SQLite · Jinja2 | [tlim-python2](https://github.com/calgadev/tlim-python2) *(current)* | ✅ Complete |
| Stage 2 — REST API rewrite | Java 17 · Spring Boot 3.5 · Spring Data JPA · PostgreSQL · Flyway | [tlim-java](https://github.com/calgadev/tlim-java) | ✅ Complete (deploy pending) |
| Stage 3 — React frontend | React 19 · TypeScript · Vite · TanStack Query · Tailwind CSS | [tlim-frontend](https://github.com/calgadev/tlim-frontend) | ✅ Complete (deploy pending) |

The project is intentionally developed in three stages with different stacks to demonstrate that the same problem can be solved across different languages and technologies — showing transferable knowledge rather than familiarity with a single tool.

---

## How this project was built

Stage 1 was developed using a three-prompt AI-assisted methodology: a **Research** prompt to explore the problem domain and existing codebase before writing any code, a **Spec** prompt to produce a detailed implementation plan file-by-file before touching the editor, and a **Code** prompt to implement exactly what the Spec described — no more, no less.

The AI was instructed never to make decisions unilaterally: every ambiguity was surfaced as a question and resolved before proceeding. To keep context small and avoid hallucination, the workflow was executed feature-by-feature — each feature got its own Research → Spec → Code cycle in a fresh session.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy 2.0 |
| Templates | Jinja2 |
| Validation | Pydantic |
| Server | Uvicorn |
| UI | Bootstrap 5 |

---

## Architecture

```
tlim-python2/
├── main.py              ← FastAPI app entry point
├── database.py          ← SQLAlchemy + SQLite configuration
├── seed.py              ← Populates the database with initial data
├── models/              ← Database tables via SQLAlchemy ORM
├── schemas/             ← Input/output validation via Pydantic
├── routers/             ← HTTP endpoints (no business logic)
├── services/            ← Business logic (sale decision, hunt import)
├── parsers/             ← Hunt Analyser text and JSON parsers
├── templates/           ← Jinja2 HTML templates
├── static/              ← CSS
└── seed_data/           ← JSON files with initial servers, items and creatures
```

---

## Key Technical Decisions

**Market price at server level** — shared across all characters on the same server, avoiding duplicate registration.

**`npc_buyable` as explicit boolean** — avoids the ambiguity of using `npc_price = 0` as a sentinel value. A price of zero and the absence of a price are meaningfully different states.

**Atomic hunt import** — all or nothing: if any item or creature in the log is missing from the database, nothing is persisted. This keeps hunt records consistent and trustworthy.

**`balance` not stored** — calculated at display time as `loot_total - supplies`, since both values are immutable after import. Storing the difference would be redundant.

**Sale decision engine** — four possible outcomes per item: Keep, Sell to NPC, Sell on market, No price available.

---

## Prerequisites

- Python 3.12+

---

## Configuration

Stage 1 uses SQLite with no external database server. No environment variables or credentials are required: the SQLite file and its tables are created automatically, and `seed.py` fills them with the initial data. Running it again skips rows that already exist.

---

## Running Locally

```bash
# Clone the repository
git clone https://github.com/calgadev/tlim-python2.git
cd tlim-python2

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Populate the database with initial data (servers, items, creatures)
python seed.py

# Start the development server
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/users/` to pick or create a user. The root path `/` only returns a health check (`{"status": "TLIM is running"}`).

> **Note:** Running `python seed.py` is required before using the application. It creates the database and populates it with 30 servers, 20 items and 20 creatures.

---

## UI Navigation
Stage 1 is a server-side rendered application: every route returns an HTML page or a redirect, and there is no JSON API (FastAPI's auto-generated `/docs` lists the routes, but they are not meant to be called directly). The selected user and character travel as `?user_id=` and `?character_id=` query params.

| Page | Path | Description |
|---|---|---|
| Users | `/users/` | Select or create a user |
| Characters | `/characters/?user_id=` | Register and list characters |
| Edit character | `/characters/{id}/edit` | Change a character's name, server or vocation |
| Hunt import | `/hunt/?user_id=&character_id=` | Paste text or upload JSON from the Hunt Analyser |
| Hunt history | `/hunt/history?user_id=&character_id=` | Past sessions of a character |
| Hunt detail | `/hunt/{id}` | Full breakdown of a single session |
| Inventory | `/inventory/?user_id=&character_id=` | Stock levels, goals, and sale decisions |
| Items & prices | `/items/` | Item list and market price management |

---

## Hunt Analyser Import

Two import modes accept hunt session data exported from the in-game Hunt Analyser:

| Mode | Format |
|---|---|
| Text paste | Raw text copied from the Hunt Analyser |
| JSON upload | JSON file exported from the Hunt Analyser |

Both formats are parsed into the same internal `ParsedHunt` dataclass before persistence. If any item or creature name in the log is not found in the database, the entire import is rejected (atomic behaviour).

---

## What is NOT in scope for Stage 1

- TibiaWiki scraping (added in Stage 2)
- JWT authentication (added in Stage 2)
- REST API / Swagger UI (Stage 2)
- React frontend (Stage 3)
- Mini wiki for items and creatures (Stage 2)
- Email, OAuth, or any auth mechanism beyond basic user selection
- Pagination

---

## Stage Checklists

### Stage 1 — Python / FastAPI / SQLite *(current)*
- [x] Project structure and virtual environment
- [x] Database configuration (SQLAlchemy + SQLite)
- [x] Base FastAPI app running with Uvicorn
- [x] 10 SQLAlchemy models (User, Server, Character, Item, Creature, ServerItemPrice, Inventory, HuntSession, HuntSessionItem, HuntSessionMonster)
- [x] Seed script (30 servers, 20 items, 20 creatures)
- [x] User and character management
- [x] Hunt session import — text and JSON formats
- [x] Hunt history and detail views
- [x] Inventory management with stock goals
- [x] Sale decision engine (Keep / Sell to NPC / Sell on market / No price available)
- [x] Market price management per server

### Stage 2 — Java / Spring Boot / PostgreSQL
- [x] Full domain model and Flyway migrations (V1–V14)
- [x] JWT authentication (register, login, stateless Bearer token, security filter chain)
- [x] Swagger UI with JWT bearer auth scheme
- [x] Official world list imported from the TibiaData API, with inactive worlds kept and flagged (`/api/servers`)
- [x] Character CRUD API with user-scoped queries (`/api/characters`)
- [x] Item API with name/category search and `?limit=` (`/api/items`)
- [x] Creature API with loot tables (`/api/creatures`)
- [x] Inventory API with stock goals (`/api/inventory`)
- [x] Hunt Sessions API with location filter (`/api/hunt-sessions`)
- [x] Hunt Analyser import — text and JSON — that adds the loot to the inventory (deleting the hunt reverts it)
- [x] Server Item Prices API — per-server market prices (`/api/servers/{serverId}/item-prices`)
- [x] Sale Decision Engine — per-character recommendations using the character's server prices
- [x] Admin API + TibiaWiki scraper (`/api/admin`)
- [x] Browser support for the frontend: CORS, uniform JSON error bodies, admin account from environment variables
- [x] Unit and web-slice tests, GitHub Actions CI
- [ ] Deploy

### Stage 3 — React / TypeScript / Vite

Developed in [tlim-frontend](https://github.com/calgadev/tlim-frontend).

- [x] Typed API layer and TanStack Query hooks synced with the Stage 2 DTOs
- [x] JWT login/register with expiry handling and route guards (USER / ADMIN)
- [x] Characters with an active-character switcher
- [x] Inventory with goals, and the sale decision view with filters and totals
- [x] Hunt Analyser import (text or JSON), hunt history and detail
- [x] Wiki for items and creatures (TibiaWiki data)
- [x] Market prices per world, world list, admin scraper panel
- [x] Vitest + Testing Library tests, route-level code splitting, GitHub Actions CI
- [ ] Deploy

---

## Sobre o projeto

O TLIM nasceu de duas dores reais de um jogador de Tibia: saber o que fazer com o loot após uma hunt, e ter histórico estruturado de sessões para comparar onde vale mais a pena caçar.

Este projeto é desenvolvido em três etapas com stacks diferentes — Python/FastAPI/SQLite, Java/Spring Boot/PostgreSQL e React/TypeScript — como demonstração de evolução técnica e capacidade de transferir conhecimento entre linguagens. A ideia central é mostrar que o mesmo problema pode ser resolvido com ferramentas diferentes, evidenciando raciocínio transferível em vez de familiaridade com uma única tecnologia.

Faz parte de uma transição de carreira de Analista de Sistemas para Desenvolvedor.

---

## Author

**Guilherme Calgaro**
Systems Analyst | AI-assisted development methodologies
[LinkedIn](https://www.linkedin.com/in/guilherme-de-oliveira-calgaro/) · [GitHub](https://github.com/calgadev)
